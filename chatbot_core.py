from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Optional, Tuple
import csv
import random
import re
import unicodedata
from difflib import SequenceMatcher
from calculators import (
    calcular_interes_compuesto, calcular_cuota_prestamo,
    plan_ahorro, tiempo_pagar_deuda, presupuesto_50_30_20,
    comparar_inversiones
)
from database import update_user_fields, get_user, get_or_create_user


# Ruta de log en el mismo directorio del archivo
LOG_PATH = Path(__file__).with_name("chat_logs.csv")


def is_night(dt: datetime) -> bool:
    return dt.time() < time(6, 0) or dt.time() >= time(20, 0)


def stamp(dt: Optional[datetime] = None) -> str:
    dt = dt or datetime.now()
    periodo = "noche" if is_night(dt) else "día"
    return f"[{dt.strftime('%H:%M')} {periodo}]"


def normalize_text(text: str) -> str:
    """
    Normaliza el texto para mejorar la detección:
    - Convierte a minúsculas
    - Elimina acentos y diacríticos
    - Preserva números y espacios
    """
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar acentos (NFD normaliza y separamos los diacríticos)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def log_interaction(ts: datetime, scenario: str, user: str, bot: str, 
                    sentiment: str = "neutral", emotion: str = "none") -> None:
    # Crear encabezado si no existe
    new_file = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "scenario", "sentiment", "emotion", "user", "bot"])
        writer.writerow([ts.isoformat(timespec='seconds'), scenario, sentiment, emotion, user, bot])


@dataclass
class BotResult:
    scenario: str
    reply: str
    when: datetime
    sentiment: str = "neutral"  # positivo, negativo, neutral
    emotion: str = "none"  # preocupado, estresado, motivado, confundido, etc.


def greeting(dt: datetime, sentiment: str = "neutral", emotion: str = "none") -> str:
    """Saludo adaptado según hora, sentimiento y emoción"""
    h = dt.hour
    
    # Saludo base según hora
    if h < 6 or h >= 20:
        base = "Buenas noches"
    elif h < 12:
        base = "Buenos días"
    elif h < 20:
        base = "Buenas tardes"
    else:
        base = "Hola"
    
    # Añadir empatía según emoción detectada
    empathy = ""
    if emotion == "preocupado":
        empathy = ", entiendo tu preocupación"
    elif emotion == "estresado":
        empathy = ", sé que es una situación estresante"
    elif emotion == "confundido":
        empathy = ", no te preocupes, te voy a ayudar paso a paso"
    elif emotion == "desesperado":
        empathy = ", tranquilo/a, vamos a encontrar una solución"
    elif emotion == "motivado":
        empathy = ", me encanta tu actitud positiva"
    elif emotion == "frustrado":
        empathy = ", entiendo tu frustración, pero hay solución"
    elif emotion == "esperanzado":
        empathy = ", ¡excelente que tengas esa meta!"
    elif sentiment == "negativo" and emotion == "none":
        empathy = ", entiendo cómo te sientes"
    elif sentiment == "positivo" and emotion == "none":
        empathy = ", ¡qué bueno!"
    
    return base + empathy


class ChatBot:
    def __init__(self):
        # Keywords ya normalizadas (sin acentos, minúsculas)
        # Ahora son más flexibles y naturales
        self.keywords = {
            "presupuesto": [
                "presupuesto", "gastos", "ingresos", "planificar", "organizar", "dinero", 
                "cuanto gasto", "administrar", "controlar", "distribuir", "plata",
                "sueldo", "salario", "cobro", "pago", "cuanto tengo", "alcanza",
                "economia domestica", "finanzas personales", "mis cuentas"
            ],
            
            "ahorro": [
                "ahorrar", "ahorro", "ahorros", "guardar", "meta", "objetivo", "juntar", "reservar",
                "quiero comprar", "necesito", "voy a comprar", "planeo", "juntando",
                "guardando", "economizar", "separar", "alcancia"
            ],
            
            "inversiones": [
                "invertir", "inversion", "inversiones", "acciones", "bonos", 
                "plazo fijo", "crypto", "criptomonedas", "fondos", "donde pongo", 
                "rentabilidad", "ganar", "multiplicar", "hacer crecer", "rendimiento", 
                "que me conviene", "mejor opcion", "aguinaldo", "sueldo anual", 
                "bonus", "prima", "cedear", "etf", "fci"
            ],
            
            "deudas": [
                "deuda", "deudas", "prestamo", "credito", "tarjeta", 
                "cuota", "intereses", "debo", "pagar", "prestan", "financiacion",
                "adeudo", "cancelar", "saldar", "cuotas", "mensualidades", "banco",
                "me atrase", "no puedo pagar", "refinanciar"
            ],
            
            "educacion": [
                "aprender", "ensenar", "explicar", "que es", "como funciona", 
                "no entiendo", "concepto", "significa", "quiere decir", "ayuda a entender",
                "me gustaria saber", "quisiera saber", "podrias explicar", "podrías explicar",
                "curso", "tutorial", "ensenanza"
            ],
            
            "calculadora": [
                "calcular", "calcula", "cuanto", "simular", "simulador",
                "en cuanto tiempo", "cuota", "plazo", "rendimiento", "comparar",
                "dame numeros", "hazme cuentas", "sacame la cuenta"
            ],
        }
        
        # Patrones de intención (frases típicas)
        self.intent_patterns = {
            "presupuesto": [
                "cobro", "gano", "tengo de sueldo", "ingreso", "me pagan",
                "cuanto me alcanza", "llegando a fin de mes", "no me alcanza"
            ],
            "ahorro": [
                "quiero comprar", "voy a comprar", "necesito juntar", "me gustaria tener",
                "planear para", "meta de", "objetivo de", "en cuanto tiempo"
            ],
            "inversiones": [
                "donde poner", "que hago con", "me conviene", "recomendas", 
                "mejor manera de", "opciones para", "puedo hacer con"
            ],
            "deudas": [
                "me quedan", "estoy pagando", "no puedo pagar", "atrasado con",
                "cuotas de", "banco me", "tarjeta me cobra"
            ],
        }
        
        # Contexto de conversación con memoria extendida
        self.last_scenario = None
        self.last_user_message = None
        self.conversation_state = {
            'waiting_for': None,  # presupuesto_monto, ahorro_objetivo, deuda_monto, etc.
            'partial_data': {},   # Datos incompletos que estamos recolectando
            'last_topic': None,   # Último tema específico (casa, auto, tarjeta, etc.)
            'turn_count': 0       # Contador de turnos para contexto
        }
        self.user_data = {}
        self.user_phone = "web_user"  # Default para web, se sobrescribe en WhatsApp
    
    def similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud entre dos textos (0.0 a 1.0)"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def analyze_sentiment(self, text: str) -> Tuple[str, str]:
        """
        Analiza el sentimiento y emoción del mensaje del usuario.
        Retorna: (sentimiento, emoción)
        """
        t = text.lower()
        
        # Palabras positivas
        positive_words = [
            "bien", "genial", "excelente", "bueno", "gracias", "perfecto", 
            "feliz", "contento", "alegre", "esperanza", "optimista", "listo",
            "quiero", "voy a", "puedo", "lograr", "éxito", "mejor", "avanzar"
        ]
        
        # Palabras negativas
        negative_words = [
            "mal", "terrible", "horrible", "preocupado", "preocupación", "angustia",
            "desesperado", "agobiado", "estresado", "triste", "miedo", "pánico",
            "crisis", "urgente", "no puedo", "imposible", "nunca", "peor"
        ]
        
        # Emociones específicas con keywords
        emotions = {
            "preocupado": ["preocupado", "preocupa", "inquieto", "nervioso", "ansioso", "intranquilo"],
            "estresado": ["estresado", "estrés", "agobiado", "presión", "sobrecargado", "no aguanto"],
            "confundido": ["confundido", "no entiendo", "perdido", "no sé", "ayuda", "como hago"],
            "desesperado": ["desesperado", "urgente", "no puedo más", "crisis", "grave", "crítico"],
            "motivado": ["motivado", "quiero", "voy a", "listo", "empezar", "comenzar", "dale"],
            "frustrado": ["frustrado", "harto", "cansado", "siempre", "otra vez", "no funciona"],
            "esperanzado": ["espero", "ojalá", "deseo", "sueño", "meta", "objetivo", "futuro"]
        }
        
        # Contar palabras positivas y negativas
        pos_count = sum(1 for word in positive_words if word in t)
        neg_count = sum(1 for word in negative_words if word in t)
        
        # Detectores de estrés financiero
        financial_stress = [
            "no me alcanza", "no llego", "no puedo pagar", "me quedé sin",
            "problemas de plata", "no tengo", "me falta", "atrasado"
        ]
        if any(phrase in t for phrase in financial_stress):
            neg_count += 2
        
        # Detectores de proactividad
        proactive = [
            "quiero aprender", "mejorar", "planear", "organizar",
            "hacer un plan", "tomar control", "cambiar"
        ]
        if any(phrase in t for phrase in proactive):
            pos_count += 2
        
        # Determinar sentimiento general
        if neg_count > pos_count:
            sentiment = "negativo"
        elif pos_count > neg_count:
            sentiment = "positivo"
        else:
            sentiment = "neutral"
        
        # Detectar emoción específica
        emotion = "none"
        emotion_score = 0
        for emot, keywords in emotions.items():
            score = sum(1 for kw in keywords if kw in t)
            if score > emotion_score:
                emotion_score = score
                emotion = emot
        
        return sentiment, emotion

    def detect(self, text: str) -> str:
        # NORMALIZAR el texto primero (sin acentos, minúsculas, etc.)
        t = normalize_text(text)
        
        # 0. Detección directa de palabras clave sueltas (mejorada con normalización)
        if len(t.split()) <= 2:
            single_word_map = {
                # Todas normalizadas (sin acentos)
                "presupuesto": "presupuesto",
                "presupuestos": "presupuesto",
                "ahorro": "ahorro",
                "ahorrar": "ahorro",
                "ahorros": "ahorro",
                "inversion": "inversiones",
                "inversiones": "inversiones",
                "invertir": "inversiones",
                "deuda": "deudas",
                "deudas": "deudas",
                "prestamo": "deudas",
                "tarjeta": "deudas",
                "educacion": "educacion",
                "aprender": "educacion",
                "calculadora": "calculadora",
                "calcular": "calculadora",
            }
            for word in t.split():
                if word in single_word_map:
                    return single_word_map[word]
        
        # 1. Si estamos esperando información específica (respuestas cortas)
        if self.conversation_state['waiting_for']:
            # Si el usuario solo pone un número o respuesta breve, mantener el contexto
            if len(t.split()) <= 3 or re.match(r'^\d+[\d\s.,]*$', t):
                return self.last_scenario or "ayuda"
        
        # 2. Detección de respuestas muy cortas con contexto
        if len(t.split()) <= 2:
            # Si solo es un número, mantener el escenario anterior
            if re.match(r'^\d+[\d\s.,]*$', t) and self.last_scenario:
                return self.last_scenario
            
            # Respuestas de continuación
            follow_up = ["sí", "si", "dale", "ok", "bueno", "claro", "genial", "perfecto"]
            if any(word in t for word in follow_up) and self.last_scenario:
                return self.last_scenario
            
            # Palabras clave de ahorro (una sola palabra)
            ahorro_keywords = ["casa", "auto", "carro", "viaje", "vacaciones", "emergencia", 
                             "vivienda", "departamento", "vehiculo"]
            if any(word in t for word in ahorro_keywords):
                return "ahorro"
            
            # Respuestas de afirmación con tema anterior
            if self.conversation_state['last_topic']:
                # Si menciona el tema anterior brevemente
                if self.conversation_state['last_topic'].lower() in t:
                    return self.last_scenario or "ayuda"
            
            # Si tenemos un escenario previo y es respuesta corta, mantenerlo
            if self.last_scenario:
                return self.last_scenario
        
        # 3. Remover palabras vacías (stop words) para mejor detección
        stop_words = {
            "el", "la", "los", "las", "un", "una", "de", "del", "al", "para", 
            "por", "con", "en", "a", "y", "o", "pero", "que", "mi", "me", "te",
            "lo", "su", "sus", "se", "si", "no", "es", "son", "muy", "mas",
            "como", "cuando", "donde", "quien", "cual"
        }
        words = [w for w in t.split() if w not in stop_words and len(w) > 2]
        normalized = " ".join(words)
        
        # 3. Detección por patrones de intención (frases completas)
        pattern_scores = {scen: 0 for scen in self.keywords.keys()}
        for scen, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in t:
                    pattern_scores[scen] += 3  # Mayor peso a patrones de intención
        
        # 4. Detección por keywords (ahora más flexible con normalización)
        keyword_scores = {scen: 0 for scen in self.keywords.keys()}
        for scen, keys in self.keywords.items():
            for keyword in keys:
                # Normalizar la keyword también
                keyword_norm = normalize_text(keyword)
                
                # Búsqueda exacta (más peso)
                if keyword_norm in t or keyword_norm in normalized:
                    keyword_scores[scen] += 2
                    continue
                
                # Búsqueda de palabras individuales de la keyword
                keyword_words = keyword_norm.split()
                if len(keyword_words) > 1:
                    # Para frases multi-palabra, verificar si todas están
                    if all(kw in t for kw in keyword_words):
                        keyword_scores[scen] += 2
                        continue
                
                # Búsqueda aproximada (para typos)
                for word in words:
                    if len(word) > 3 and self.similarity(word, keyword_norm) > 0.85:
                        keyword_scores[scen] += 1
        
        # 5. Combinar puntuaciones
        total_scores = {}
        for scen in self.keywords.keys():
            total_scores[scen] = pattern_scores[scen] + keyword_scores[scen]
        
        # 5.5 Boost de educación si hay palabras educativas
        educational_triggers = ["que es", "como funciona", "explicar", "explicame", 
                               "ensenar", "aprender", "sobre", "acerca de"]
        if any(trigger in t for trigger in educational_triggers):
            # Si es una pregunta educativa, pero también matchea otro escenario fuerte
            # Dejar que el otro escenario gane si tiene buen score
            if total_scores.get('educacion', 0) > 0:
                # Solo dar boost si no hay otro escenario con score alto
                max_other = max([score for scen, score in total_scores.items() 
                               if scen != 'educacion'], default=0)
                if max_other < 2:  # Si otros escenarios son débiles
                    total_scores['educacion'] += 1
        
        # 6. Retornar el mejor match
        best = max(total_scores.items(), key=lambda x: x[1])
        if best[1] > 0:
            return best[0]
        
        # 7. Detección por contexto semántico (análisis simple)
        # Si habla de números grandes → presupuesto o ahorro
        if re.search(r'\d{5,}', t):  # Números de 5+ dígitos
            if any(w in t for w in ["debo", "deb", "pagar", "cuota"]):
                return "deudas"
            elif any(w in t for w in ["quiero", "comprar", "juntar", "necesito"]):
                return "ahorro"
            else:
                return "presupuesto"
        
        # Si hace preguntas → educación
        if any(w in t for w in ["qué", "que", "cómo", "como", "por qué", "porque", "significa"]):
            return "educacion"
        
        return "ayuda"

    def handle_presupuesto(self, text: str, dt: datetime) -> str:
        m = re.search(r"\$?\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)", text)
        
        if m:
            monto_str = m.group(1).replace(",", "")
            monto = float(monto_str.replace(".", ""))
            self.user_data['ingreso'] = monto
            # Persistir ingreso mensual del usuario
            try:
                update_user_fields(getattr(self, 'user_phone', 'web_user'), monthly_income=monto)
            except Exception:
                pass
            self.conversation_state['waiting_for'] = None
            self.conversation_state['partial_data'] = {}
            
            # Calcular distribución
            necesidades = monto * 0.50
            personales = monto * 0.30
            ahorro = monto * 0.20
            
            return (
                f"¡Excelente! Con ingresos de ${monto:,.0f}, te sugiero la regla 50/30/20:\n\n"
                f"💵 Necesidades básicas (50%): ${necesidades:,.0f}\n"
                f"   → Vivienda, comida, servicios, transporte\n\n"
                f"🎭 Gastos personales (30%): ${personales:,.0f}\n"
                f"   → Entretenimiento, salidas, hobbies\n\n"
                f"🏦 Ahorro/Inversión (20%): ${ahorro:,.0f}\n"
                f"   → Fondo emergencia, metas, inversiones\n\n"
                f"¿Quieres ajustar estos porcentajes o que te ayude con algo específico?"
            )
        else:
            # Marcamos que estamos esperando el monto
            self.conversation_state['waiting_for'] = 'presupuesto_monto'
            return (
                f"¡Perfecto! Para crear un presupuesto necesito saber:\n\n"
                f"💰 ¿Cuáles son tus ingresos mensuales?\n\n"
                f"Escribe el monto (ej: 50000 o $50000) y te armo un plan personalizado 📊"
            )


    def handle_ahorro(self, text: str, dt: datetime) -> str:
        # Detectar metas específicas
        metas_detectadas = []
        if any(w in text.lower() for w in ["auto", "carro", "vehiculo"]):
            metas_detectadas.append("🚗 Auto")
        if any(w in text.lower() for w in ["casa", "vivienda", "departamento"]):
            metas_detectadas.append("🏠 Vivienda")
        if any(w in text.lower() for w in ["viaje", "viajar", "vacaciones"]):
            metas_detectadas.append("✈️ Viaje")
        if any(w in text.lower() for w in ["emergencia", "imprevisto"]):
            metas_detectadas.append("🆘 Fondo de emergencia")
        
        # Extraer monto objetivo si existe
        m = re.search(r"\$?\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)", text)
        
        if metas_detectadas:
            meta_str = " y ".join(metas_detectadas)
            # Guardar la meta en el contexto
            self.conversation_state['last_topic'] = metas_detectadas[0]
            
            respuesta = f"¡Excelente meta: {meta_str}! 🎯\n\n"
            
            if m:
                monto_str = m.group(1).replace(",", "")
                objetivo = float(monto_str.replace(".", ""))
                self.conversation_state['waiting_for'] = None
                self.conversation_state['partial_data'] = {}
                
                # Calcular tiempos de ahorro
                mes_10 = objetivo / 10
                mes_15 = objetivo / 15
                mes_20 = objetivo / 20
                
                respuesta += (
                    f"Para ahorrar ${objetivo:,.0f}:\n\n"
                    f"📅 En 10 meses: ahorra ${mes_10:,.0f}/mes\n"
                    f"📅 En 15 meses: ahorra ${mes_15:,.0f}/mes\n"
                    f"📅 En 20 meses: ahorra ${mes_20:,.0f}/mes\n\n"
                    f"💡 Tip: Automatiza una transferencia el día que cobras.\n"
                    f"¿En cuánto tiempo quieres lograrlo?"
                )
            else:
                # Guardamos la meta pero falta el monto
                self.conversation_state['waiting_for'] = 'ahorro_monto'
                self.conversation_state['partial_data']['meta'] = meta_str
                respuesta += f"¿Cuánto necesitas ahorrar para {meta_str}?"
            
            return respuesta
        
        # Si no detectamos meta, verificar si tenemos contexto previo
        if self.conversation_state['waiting_for'] == 'ahorro_monto' and m:
            monto_str = m.group(1).replace(",", "")
            objetivo = float(monto_str.replace(".", ""))
            meta_str = self.conversation_state['partial_data'].get('meta', 'tu meta')
            self.conversation_state['waiting_for'] = None
            self.conversation_state['partial_data'] = {}
            
            mes_10 = objetivo / 10
            mes_15 = objetivo / 15
            mes_20 = objetivo / 20
            
            return (
                f"Perfecto! Para ahorrar ${objetivo:,.0f} para {meta_str}:\n\n"
                f"📅 En 10 meses: ahorra ${mes_10:,.0f}/mes\n"
                f"📅 En 15 meses: ahorra ${mes_15:,.0f}/mes\n"
                f"📅 En 20 meses: ahorra ${mes_20:,.0f}/mes\n\n"
                f"💡 Tip: Automatiza una transferencia el día que cobras.\n"
                f"¿En cuánto tiempo quieres lograrlo?"
            )
        
        consejos = [
            "Automatiza tu ahorro: Programa transferencias automáticas el día que cobras.",
            "Método de los sobres: Divide tu dinero en sobres por categoría.",
            "Regla 24 horas: Espera 24h antes de compras no planificadas.",
            "Challenge 52 semanas: Semana 1 ahorra $100, semana 2 $200, y así..."
        ]
        consejo = random.choice(consejos)
        
        return (
            f"¡Genial que quieras ahorrar! 🏦\n\n"
            f"💡 {consejo}\n\n"
            f"Metas populares:\n"
            f"• 🆘 Fondo emergencia: 3-6 meses de gastos\n"
            f"• ✈️ Viaje/Vacaciones: 3-12 meses\n"
            f"• 🚗 Auto: 1-3 años\n"
            f"• 🏠 Vivienda: 5-10 años\n\n"
            f"¿Para qué quieres ahorrar? Escribe tu meta y el monto."
        )

    def handle_inversiones(self, text: str, dt: datetime) -> str:
        t = text.lower()

        # Detectar nivel de experiencia
        principiante = any(w in t for w in ["principiante", "comienzo", "empezar", "nuevo", "nunca invertí", "primera vez"])
        conservador = any(w in t for w in ["seguro", "sin riesgo", "conservador", "tranquilo", "no arriesgar"])
        agresivo = any(w in t for w in ["agresivo", "riesgo alto", "cripto", "acciones", "rápido"])

        # Extraer números y desambiguar horizonte vs monto
        nums_raw = re.findall(r"\d+(?:[.,]\d+)?", text)
        nums = [float(n.replace('.', '').replace(',', '')) for n in nums_raw]
        monto: Optional[float] = None
        horizonte_meses: Optional[int] = None

        # Heurísticas de horizonte
        if any(k in t for k in ["mes", "meses", "m."]):
            candidatos = [int(x) for x in nums if x <= 120]
            if candidatos:
                horizonte_meses = candidatos[0]
        if any(k in t for k in ["año", "años", "anio", "anios"]):
            candidatos = [int(x) for x in nums if x <= 50]
            if candidatos:
                horizonte_meses = candidatos[0] * 12

        # Heurísticas de monto: elegir el mayor número que no sea el horizonte
        if nums:
            candidates = nums.copy()
            if horizonte_meses is not None and float(horizonte_meses) in candidates:
                candidates.remove(float(horizonte_meses))
            if candidates:
                monto = max(candidates)

        # Recuperar contexto previo de inversiones si existe
        inv_ctx = self.conversation_state['partial_data'].get('inversion', {})
        if monto is None and 'monto' in inv_ctx:
            monto = inv_ctx['monto']
        if horizonte_meses is None and 'horizonte_meses' in inv_ctx:
            horizonte_meses = inv_ctx['horizonte_meses']

        respuesta = "📈 Opciones de inversión:\n\n"
        
        if principiante or conservador:
            respuesta += (
                "Para empezar de forma segura:\n\n"
                "🟢 Bajo Riesgo (ideal para principiantes):\n"
                "• Plazo fijo: 6-12% anual, 100% seguro\n"
                "• FCI Money Market: Liquidez diaria, bajo riesgo\n"
                "• Bonos del Estado: Rendimiento predecible\n\n"
            )
        
        if not conservador or agresivo:
            respuesta += (
                "🟡 Riesgo Moderado (diversificado):\n"
                "• ETFs globales: Diversificación automática\n"
                "• Fondos balanceados: Mix de bonos y acciones\n"
                "• CEDEARs: Acciones extranjeras en pesos\n\n"
            )
        
        if agresivo:
            respuesta += (
                "🔴 Alto Riesgo (solo dinero que puedas perder):\n"
                "• Acciones individuales: Alta volatilidad\n"
                "• Criptomonedas: Riesgo extremo, alto potencial\n"
                "• Trading: Requiere conocimiento técnico\n\n"
            )
        # Persistir perfil de riesgo sugerido si el usuario lo expresa
        try:
            if conservador:
                update_user_fields(getattr(self, 'user_phone', 'web_user'), risk_profile='conservador')
            elif agresivo:
                update_user_fields(getattr(self, 'user_phone', 'web_user'), risk_profile='agresivo')
        except Exception:
            pass
        
        if monto is not None:
            respuesta += (
                f"💰 Con ${monto:,.0f} podrías:\n"
                f"• Diversificar en 3-4 instrumentos\n"
                f"• Invertir progresivamente (DCA)\n"
                f"• Empezar conservador y aumentar riesgo\n\n"
            )

        if horizonte_meses is not None:
            años = horizonte_meses / 12
            respuesta += f"🕒 Horizonte: {horizonte_meses} meses ({años:.1f} años)\n\n"

        # Guardar contexto parcial de inversiones
        if monto is not None or horizonte_meses is not None:
            self.conversation_state['partial_data']['inversion'] = {
                'monto': monto if monto is not None else inv_ctx.get('monto'),
                'horizonte_meses': horizonte_meses if horizonte_meses is not None else inv_ctx.get('horizonte_meses')
            }

        # Detectar confirmación para simular
        confirm_words = ["dale", "si", "sí", "ok", "okay", "listo", "perfecto", "genial", "hace", "hazlo", "simula", "simular"]
        wants_simulation = any(w in t for w in confirm_words) or ("simular" in t or "simula" in t)

        # Si tenemos suficiente contexto y el usuario confirma, simular con defaults si no dio tasa/aporte
        if wants_simulation and self.conversation_state['partial_data'].get('inversion'):
            inv = self.conversation_state['partial_data']['inversion']
            if inv.get('monto') and inv.get('horizonte_meses'):
                capital = float(inv['monto'])
                años = max(0.1, inv['horizonte_meses'] / 12)

                # Intentar extraer tasa y aporte del mensaje actual
                tasa = None
                aporte = None
                # Busca patrones simples tipo "12%" o "tasa 12"
                m_tasa_pct = re.search(r"(\d+[.,]?\d*)\s*%", t)
                if m_tasa_pct:
                    tasa = float(m_tasa_pct.group(1).replace(',', '.'))
                else:
                    m_tasa_kw = re.search(r"tasa\s*(\d+[.,]?\d*)", t)
                    if m_tasa_kw:
                        tasa = float(m_tasa_kw.group(1).replace(',', '.'))

                # Busca "aporte" o "mensual" seguido de número
                m_aporte = re.search(r"(aporte|mensual)\D*(\d+[.,]?\d*)", t)
                if m_aporte:
                    aporte = float(m_aporte.group(2).replace(',', '.'))

                tasa = tasa if tasa is not None else 12.0
                aporte = aporte if aporte is not None else 0.0

                resultado = calcular_interes_compuesto(capital, tasa, años, aporte)
                sim = (
                    f"🧮 Simulación con interés compuesto:\n\n"
                    f"💰 Capital inicial: ${capital:,.0f}\n"
                    f"🕒 Plazo: {años:.1f} años ({int(años*12)} meses)\n"
                    f"📈 Tasa: {tasa}% anual\n"
                    f"💸 Aporte mensual: ${aporte:,.0f}\n\n"
                    f"🎯 Resultado:\n"
                    f"• Total invertido: ${resultado['total_invertido']:,.0f}\n"
                    f"• Monto final: ${resultado['monto_final']:,.0f}\n"
                    f"• Ganancia: ${resultado['ganancia']:,.0f} ({resultado['rendimiento_porcentaje']}%)\n\n"
                )

                sim += "¿Querés ajustar la tasa o agregar un aporte mensual distinto? Dime, por ejemplo: 'tasa 15% y aporte 10000'."
                return respuesta + sim

        # Si falta horizonte o monto, pedir lo que falte
        if monto is None and horizonte_meses is None:
            return (
                respuesta +
                "Para personalizarlo, decime: \n"
                "• Monto a invertir (ej: 150000)\n"
                "• Horizonte (ej: 7 meses o 2 años)\n"
            )
        if monto is None:
            return respuesta + "¿Con qué monto querés empezar a invertir? (ej: $150000)"
        if horizonte_meses is None:
            return respuesta + "¿Cuánto tiempo puedes dejar el dinero invertido? (ej: 7 meses o 2 años)"

        # Si tenemos ambos datos pero no pidió simular explícitamente, invitar a simular
        return (
            respuesta +
            "¿Querés que simulemos interés compuesto? Podés decir 'dale' o indicar 'tasa 12% y aporte 0'."
        )

    def handle_deudas(self, text: str, dt: datetime) -> str:
        m = re.search(r"\$?\s*(\d+(?:[.,]\d{3})*(?:[.,]\d{2})?)", text)
        t = text.lower()
        
        # Detectar tipo de deuda
        tarjeta = any(w in t for w in ["tarjeta", "crédito", "visa", "mastercard"])
        prestamo = any(w in t for w in ["préstamo", "prestamo", "banco"])
        multiple = any(w in t for w in ["varias", "muchas", "múltiples", "multiples"])
        
        respuesta = ""
        
        if m:
            monto_str = m.group(1).replace(",", "")
            deuda = float(monto_str.replace(".", ""))
            self.user_data['deuda'] = deuda
            # Persistir deuda total si aplica
            try:
                update_user_fields(getattr(self, 'user_phone', 'web_user'), total_debt=deuda)
            except Exception:
                pass
            
            # Si estábamos esperando el pago mensual, guardar ambos datos
            if self.conversation_state['waiting_for'] == 'deuda_pago':
                pago_mensual = deuda
                deuda = self.conversation_state['partial_data'].get('deuda_total', 0)
                meses = deuda / pago_mensual if pago_mensual > 0 else 0
                self.conversation_state['waiting_for'] = None
                self.conversation_state['partial_data'] = {}
                
                return (
                    f"Perfecto! Con una deuda de ${deuda:,.0f} y pagos de ${pago_mensual:,.0f}/mes:\n\n"
                    f"📅 Liquidarás tu deuda en {meses:.0f} meses\n"
                    f"💰 Total a pagar: ${deuda:,.0f}\n\n"
                    f"💡 Tip: Si puedes aumentar aunque sea $1000/mes, ahorrarás mucho en intereses.\n"
                    f"¿Quieres que calcule con otro monto mensual?"
                )
            
            # Calcular planes de pago
            meses_6 = deuda / 6
            meses_12 = deuda / 12
            meses_18 = deuda / 18
            
            respuesta = f"Entiendo, tienes una deuda de ${deuda:,.0f}. ¡Vamos a resolverlo! 💪\n\n"
            
            if tarjeta:
                respuesta += (
                    f"💳 Estrategias para deuda de tarjeta:\n"
                    f"1. Llama al banco y negocia la tasa (muchos aceptan)\n"
                    f"2. Pasa a un préstamo personal (tasa más baja)\n"
                    f"3. Deja de usarla hasta saldar\n\n"
                )
            
            respuesta += (
                f"📅 Planes de pago sugeridos:\n"
                f"• 6 meses: ${meses_6:,.0f}/mes (rápido pero intenso)\n"
                f"• 12 meses: ${meses_12:,.0f}/mes (equilibrado)\n"
                f"• 18 meses: ${meses_18:,.0f}/mes (más manejable)\n\n"
            )
            
            # Si conocemos el ingreso
            if 'ingreso' in self.user_data:
                porcentaje = (meses_12 / self.user_data['ingreso']) * 100
                respuesta += f"Con tus ingresos, pagar en 12 meses sería el {porcentaje:.0f}% de tu sueldo.\n\n"
            
            # Preguntar cuánto puede pagar mensualmente
            self.conversation_state['waiting_for'] = 'deuda_pago'
            self.conversation_state['partial_data']['deuda_total'] = deuda
            respuesta += "¿Cuánto puedes pagar mensualmente?"
        
        else:
            respuesta = "Entiendo que tienes deudas. No te preocupes, hay solución. 💪\n\n"
        
        if multiple or not m:
            respuesta += (
                f"🎯 Método Bola de Nieve (muy efectivo):\n"
                f"1. Lista TODAS tus deudas de menor a mayor\n"
                f"2. Paga el mínimo en todas\n"
                f"3. A la más chica, dale TODO extra que puedas\n"
                f"4. Al pagarla, esa plata va a la siguiente\n"
                f"5. Efecto motivador al ver progreso rápido\n\n"
            )
        
        respuesta += (
            "💡 Acciones inmediatas:\n"
            "• Corta gastos superfluos temporalmente\n"
            "• Busca ingresos extras (freelance, venta)\n"
            "• Negocia tasas con los bancos\n"
            "• No pidas más crédito mientras pagas\n\n"
            "¿Cuánto puedes destinar mensualmente a pagar deudas?"
        )
        
        return respuesta

    def handle_calculadora(self, text: str, dt: datetime) -> str:
        """Maneja consultas que requieren cálculos financieros"""
        t = text.lower()
        
        # Extraer todos los números del texto
        numeros = re.findall(r'\d+(?:[.,]\d+)?', text)
        nums = [float(n.replace(',', '')) for n in numeros]
        
        # Detectar tipo de cálculo
        if any(w in t for w in ["interes compuesto", "invertir", "rendimiento", "cuanto ganaria"]):
            if len(nums) >= 2:
                capital = nums[0]
                años = nums[1] if len(nums) > 1 else 5
                tasa = nums[2] if len(nums) > 2 else 12.0
                aporte = nums[3] if len(nums) > 3 else 0
                
                resultado = calcular_interes_compuesto(capital, tasa, años, aporte)
                
                return (
                    f"📊 Simulación de Inversión:\n\n"
                    f"💰 Capital inicial: ${capital:,.0f}\n"
                    f"📅 Plazo: {años} años\n"
                    f"📈 Tasa: {tasa}% anual\n"
                    f"💸 Aporte mensual: ${aporte:,.0f}\n\n"
                    f"🎯 RESULTADO:\n"
                    f"• Total invertido: ${resultado['total_invertido']:,.0f}\n"
                    f"• Monto final: ${resultado['monto_final']:,.0f}\n"
                    f"• Ganancia: ${resultado['ganancia']:,.0f} ({resultado['rendimiento_porcentaje']}%)\n\n"
                    f"💡 Tip: El interés compuesto es tu mejor aliado a largo plazo!"
                )
        
        elif any(w in t for w in ["cuota", "prestamo", "préstamo", "financiar"]):
            if len(nums) >= 2:
                monto = nums[0]
                meses = int(nums[1]) if len(nums) > 1 else 12
                tasa = nums[2] if len(nums) > 2 else 50.0
                
                resultado = calcular_cuota_prestamo(monto, tasa, meses)
                
                return (
                    f"📊 Simulación de Préstamo:\n\n"
                    f"💰 Monto solicitado: ${monto:,.0f}\n"
                    f"📅 Plazo: {meses} meses ({meses/12:.1f} años)\n"
                    f"📈 Tasa: {tasa}% anual\n\n"
                    f"🎯 RESULTADO:\n"
                    f"• Cuota mensual: ${resultado['cuota_mensual']:,.0f}\n"
                    f"• Total a pagar: ${resultado['total_a_pagar']:,.0f}\n"
                    f"• Intereses: ${resultado['intereses_totales']:,.0f}\n\n"
                    f"⚠️ Los intereses representan el {(resultado['intereses_totales']/monto)*100:.1f}% del préstamo.\n"
                    f"💡 Tip: Si puedes pagar más rápido, pagarás menos intereses."
                )
        
        elif any(w in t for w in ["pagar deuda", "cuanto tiempo", "salir de deuda"]):
            if len(nums) >= 2:
                deuda = nums[0]
                pago = nums[1]
                tasa = nums[2] if len(nums) > 2 else 0
                
                resultado = tiempo_pagar_deuda(deuda, pago, tasa)
                
                if "error" in resultado:
                    return f"⚠️ {resultado['error']}"
                
                return (
                    f"📊 Plan de Pago de Deuda:\n\n"
                    f"💳 Deuda actual: ${deuda:,.0f}\n"
                    f"💸 Pago mensual: ${pago:,.0f}\n"
                    f"📈 Interés: {tasa}% anual\n\n"
                    f"🎯 RESULTADO:\n"
                    f"• Tiempo: {resultado['meses_necesarios']} meses ({resultado['años']} años)\n"
                    f"• Total a pagar: ${resultado['total_a_pagar']:,.0f}\n"
                    f"• Intereses: ${resultado['intereses_totales']:,.0f}\n\n"
                    f"💡 Tip: Si pagas ${pago*1.5:,.0f}/mes, terminarías en {int(resultado['meses_necesarios']*0.67)} meses!"
                )
        
        elif any(w in t for w in ["comparar", "opciones", "mejor inversion"]):
            if len(nums) >= 1:
                monto = nums[0]
                años = nums[1] if len(nums) > 1 else 5
                
                opciones = comparar_inversiones(monto, int(años))
                
                respuesta = f"📊 Comparación de Inversiones:\n\n"
                respuesta += f"💰 Monto: ${monto:,.0f} por {años} años\n\n"
                
                for op in opciones[:5]:  # Top 5
                    respuesta += (
                        f"• {op['nombre']} ({op['riesgo']}):\n"
                        f"  Ganancia: ${op['ganancia']:,.0f} ({op['tasa_anual']}% anual)\n"
                        f"  Total: ${op['monto_final']:,.0f}\n\n"
                    )
                
                respuesta += "💡 Recuerda: Mayor rendimiento = Mayor riesgo"
                return respuesta
        
        # Si no se pudo identificar el cálculo
        return (
            "🧮 Calculadora Financiera\n\n"
            "Puedo ayudarte a calcular:\n\n"
            "📈 Interés compuesto:\n"
            "  'Cuanto ganaria si invierto 100000 por 5 años al 12%'\n\n"
            "💳 Cuota de préstamo:\n"
            "  'Cuanta es la cuota de 50000 en 12 meses al 50%'\n\n"
            "📅 Tiempo de pago:\n"
            "  'En cuanto tiempo pago 30000 si pago 5000 por mes'\n\n"
            "⚖️ Comparar inversiones:\n"
            "  'Comparar opciones para invertir 200000 por 10 años'\n\n"
            "Escribe tu consulta con números específicos."
        )

    def handle_educacion(self, text: str, dt: datetime) -> str:
        # Normalizar para mejor detección
        t = normalize_text(text)
        
        # Detectar conceptos específicos (ya normalizados)
        if "inflacion" in t:
            return (
                "📚 La inflación es el aumento generalizado de precios.\n\n"
                "¿Qué significa?\n"
                "• Tu dinero pierde poder de compra con el tiempo\n"
                "• Lo que hoy cuesta $100, mañana cuesta $110\n\n"
                "Cómo protegerte:\n"
                "✅ Invierte tu dinero (que crezca más que la inflación)\n"
                "✅ No guardes todo en efectivo\n"
                "✅ Compra activos que suban con la inflación\n\n"
                "¿Quieres saber sobre inversiones anti-inflación?"
            )
        
        if "interes" in t:
            return (
                "📚 Tipos de interés:\n\n"
                "🟢 Interés Simple:\n"
                "Se calcula solo sobre el capital inicial\n"
                "Ejemplo: $1000 al 10% anual = $100/año\n\n"
                "🔵 Interés Compuesto (el más poderoso):\n"
                "Se calcula sobre capital + intereses acumulados\n"
                "Ejemplo año 1: $1000 → $1100\n"
                "Año 2: $1100 → $1210 (no $1200)\n\n"
                "💡 Einstein dijo: 'El interés compuesto es la fuerza más poderosa del universo'\n\n"
                "¿Quieres calcular cuánto crecería tu inversión?"
            )
        
        if "diversificacion" in t or "diversificar" in t:
            return (
                "📚 Diversificación: No pongas todos los huevos en la misma canasta 🥚\n\n"
                "¿Qué es?\n"
                "• Repartir tu dinero en diferentes inversiones\n"
                "• Si una baja, las otras compensan\n\n"
                "Ejemplo básico:\n"
                "• 40% Bonos (bajo riesgo)\n"
                "• 40% Acciones (riesgo medio)\n"
                "• 20% Cripto/otros (alto riesgo)\n\n"
                "💡 Nunca dependas de una sola inversión.\n\n"
                "¿Quieres que te ayude a armar una estrategia diversificada?"
            )
        
        if "oro" in t:
            return (
                "📚 El Oro como Inversión 🥇\n\n"
                "Ventajas:\n"
                "✅ Refugio en crisis económicas\n"
                "✅ Protección contra inflación\n"
                "✅ Valor reconocido mundialmente\n\n"
                "Desventajas:\n"
                "❌ No genera intereses ni dividendos\n"
                "❌ Costos de almacenamiento\n"
                "❌ Volatilidad a corto plazo\n\n"
                "Formas de invertir:\n"
                "• Oro físico (lingotes, monedas)\n"
                "• ETFs de oro (más líquido)\n"
                "• Acciones mineras de oro\n\n"
                "💡 Recomendado: 5-10% de tu portafolio en oro.\n\n"
                "¿Te interesa saber sobre otras inversiones?"
            )
        
        # Ahorro e inversión (detectar ANTES del menú genérico)
        if any(word in t for word in ["ahorro", "ahorrar", "sobre ahorro"]):
            return (
                "📚 Ahorro vs Inversión: ¿Cuál es la diferencia?\n\n"
                "🏦 AHORRO:\n"
                "• Guardar dinero sin riesgo\n"
                "• Acceso inmediato\n"
                "• Poco o nulo rendimiento\n"
                "• Para emergencias y metas corto plazo\n\n"
                "📈 INVERSIÓN:\n"
                "• Hacer crecer tu dinero\n"
                "• Puede tener riesgo\n"
                "• Mayor rendimiento potencial\n"
                "• Para metas largo plazo (5+ años)\n\n"
                "💡 Necesitas AMBOS: Primero ahorra para emergencias, luego invierte.\n\n"
                "¿Quieres ayuda para empezar a ahorrar o invertir?"
            )
        
        # Tarjetas de crédito
        if "tarjeta" in t or "credito" in t:
            return (
                "📚 Tarjetas de Crédito: Cómo funcionan 💳\n\n"
                "¿Qué es?\n"
                "• Préstamo del banco que pagas después\n"
                "• NO es tu dinero, es deuda\n\n"
                "⚠️ CUIDADO con:\n"
                "• Pagar solo el mínimo (intereses altísimos)\n"
                "• Financiar en cuotas todo\n"
                "• Sacar adelantos en efectivo\n\n"
                "✅ Usa bien:\n"
                "• Paga TODO antes del vencimiento\n"
                "• Úsala para gastos planificados\n"
                "• Aprovecha beneficios y puntos\n\n"
                "💡 Si no podés pagar todo, mejor no la uses.\n\n"
                "¿Tenés deudas en tarjeta que necesites organizar?"
            )
        
        # Respuesta genérica solo si no matcheó nada
        return (
            "🎓 Centro de Educación Financiera\n\n"
            "Conceptos que puedo explicarte:\n\n"
            "💹 Inflación - Cómo protegerte\n"
            "💰 Interés simple vs compuesto\n"
            "📊 Diversificación de inversiones\n"
            "🥇 Oro como inversión\n"
            "💳 Tarjetas de crédito\n"
            "🏦 Ahorro vs inversión\n\n"
            "Preguntame sobre cualquiera de estos temas.\n"
            "Por ejemplo: 'Qué es la inflación' o 'Sobre ahorro'"
        )

    def handle_help(self, text: str, dt: datetime) -> str:
        return (
            "¡Hola! Soy tu asistente de educación financiera personal 💰\n\n"
            "¿En qué puedo ayudarte?\n\n"
            "📊 Presupuesto - Organiza ingresos y gastos\n"
            "🏦 Ahorro - Metas y estrategias\n"
            "📈 Inversiones - Guía según tu perfil\n"
            "💳 Deudas - Planes para salir\n"
            "🧮 Calculadora - Simuladores financieros\n"
            "🎓 Educación - Conceptos financieros\n\n"
            "💬 Ejemplos de lo que puedes decirme:\n"
            "• 'Presupuesto con $50000'\n"
            "• 'Quiero ahorrar para un auto'\n"
            "• 'Invertir mi aguinaldo'\n"
            "• 'Tengo deuda de $30000'\n"
            "• 'Qué es la inflación'\n\n"
            "Escribe tu consulta naturalmente ✨"
        )

    def process(self, user_text: str, when: Optional[datetime] = None) -> BotResult:
        when = when or datetime.now()
        
        # Incrementar el contador de turnos
        self.conversation_state['turn_count'] += 1
        # Cargar/crear perfil DB y pre-cargar datos útiles al estado (si existen)
        if getattr(self, 'user_phone', None):
            try:
                db_user = get_or_create_user(self.user_phone)
                if db_user.monthly_income and 'ingreso' not in self.user_data:
                    self.user_data['ingreso'] = db_user.monthly_income
            except Exception:
                pass
        
        # Analizar sentimiento y emoción
        sentiment, emotion = self.analyze_sentiment(user_text)
        
        # Detectar escenario
        scenario = self.detect(user_text)
        
        # Generar respuesta según escenario
        if scenario == "presupuesto":
            main = self.handle_presupuesto(user_text, when)
        elif scenario == "ahorro":
            main = self.handle_ahorro(user_text, when)
        elif scenario == "inversiones":
            main = self.handle_inversiones(user_text, when)
        elif scenario == "deudas":
            main = self.handle_deudas(user_text, when)
        elif scenario == "calculadora":
            main = self.handle_calculadora(user_text, when)
        elif scenario == "educacion":
            main = self.handle_educacion(user_text, when)
        else:
            main = self.handle_help(user_text, when)

        # Añadir mensaje de apoyo emocional si es necesario
        emotional_support = ""
        if sentiment == "negativo":
            if emotion == "desesperado":
                emotional_support = "\n\n💪 Recuerda: toda situación financiera tiene solución. Vamos paso a paso."
            elif emotion == "estresado":
                emotional_support = "\n\n🧘 Respira. Tomar control de tus finanzas reduce el estrés. Ya diste el primer paso."
            elif emotion == "frustrado":
                emotional_support = "\n\n✨ Entiendo tu frustración. Cada pequeño cambio suma. ¡No te rindas!"
            elif emotion == "preocupado":
                emotional_support = "\n\n🌟 La preocupación es normal, pero con un buen plan todo es más manejable."
        elif sentiment == "positivo" and emotion == "motivado":
            emotional_support = "\n\n🚀 ¡Me encanta tu energía! Con esa actitud vas a lograr tus metas."

        # Guardar último escenario para contexto
        self.last_scenario = scenario
        
        # Construir respuesta completa
        # Solo saludar en el primer turno, después responder directo
        if self.conversation_state['turn_count'] == 1:
            reply = f"{greeting(when, sentiment, emotion)}. {main}{emotional_support}"
        else:
            reply = f"{main}{emotional_support}"
        
        # Log con sentimiento y emoción
        log_interaction(when, scenario, user_text, reply, sentiment, emotion)
        
        return BotResult(
            scenario=scenario, 
            reply=reply, 
            when=when,
            sentiment=sentiment,
            emotion=emotion
        )
