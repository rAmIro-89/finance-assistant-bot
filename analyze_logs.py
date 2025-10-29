"""
Script para analizar logs de interacciones y detectar errores/patrones
Uso: python analyze_logs.py
"""
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def load_logs(csv_path="chat_logs.csv"):
    """Carga el CSV de logs"""
    logs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    return logs


def analyze_misclassifications(logs):
    """Detecta posibles clasificaciones incorrectas"""
    print("\n" + "="*80)
    print("🔍 ANÁLISIS DE CLASIFICACIONES INCORRECTAS")
    print("="*80)
    
    # Palabras clave que deberían mapear a escenarios específicos
    keywords_map = {
        'inversiones': ['invertir', 'inversion', 'inversiones', 'aguinaldo', 'plazo fijo'],
        'ahorro': ['ahorrar', 'ahorro', 'guardar', 'juntar'],
        'presupuesto': ['presupuesto', 'gastos', 'ingresos'],
        'deudas': ['deuda', 'préstamo', 'prestamo', 'tarjeta'],
        'educacion': ['aprender', 'enseñar', 'explicar', 'que es', 'como funciona']
    }
    
    misclassified = []
    
    for log in logs:
        user_msg = log['user'].lower()
        detected_scenario = log['scenario']
        
        # Verificar si hay palabras clave que sugieren otro escenario
        for expected_scenario, keywords in keywords_map.items():
            if any(kw in user_msg for kw in keywords):
                if detected_scenario != expected_scenario and detected_scenario == 'ayuda':
                    misclassified.append({
                        'timestamp': log['timestamp'],
                        'user_msg': log['user'],
                        'detected': detected_scenario,
                        'should_be': expected_scenario,
                        'keywords_found': [kw for kw in keywords if kw in user_msg]
                    })
    
    if misclassified:
        print(f"\n❌ Se encontraron {len(misclassified)} posibles errores de clasificación:\n")
        for i, item in enumerate(misclassified[:10], 1):  # Mostrar top 10
            print(f"{i}. [{item['timestamp'][:16]}]")
            print(f"   Mensaje: '{item['user_msg']}'")
            print(f"   Detectó: {item['detected']} ❌")
            print(f"   Debería ser: {item['should_be']} ✅")
            print(f"   Keywords: {', '.join(item['keywords_found'])}")
            print()
    else:
        print("\n✅ No se detectaron errores obvios de clasificación")
    
    return misclassified


def analyze_sentiment(logs):
    """Analiza distribución de sentimientos"""
    print("\n" + "="*80)
    print("😊 ANÁLISIS DE SENTIMIENTOS")
    print("="*80)
    
    sentiments = Counter(log['sentiment'] for log in logs)
    emotions = Counter(log['emotion'] for log in logs if log['emotion'] != 'none')
    
    print(f"\n📊 Distribución de sentimientos:")
    total = sum(sentiments.values())
    for sent, count in sentiments.most_common():
        pct = (count/total)*100
        print(f"  {sent:10} {count:4} mensajes ({pct:5.1f}%)")
    
    print(f"\n🎭 Emociones detectadas:")
    if emotions:
        for emo, count in emotions.most_common():
            print(f"  {emo:12} {count:4} veces")
    else:
        print("  No se detectaron emociones específicas")


def analyze_scenarios(logs):
    """Analiza distribución de escenarios"""
    print("\n" + "="*80)
    print("📋 ANÁLISIS DE ESCENARIOS")
    print("="*80)
    
    scenarios = Counter(log['scenario'] for log in logs)
    
    print(f"\n📊 Escenarios más consultados:")
    total = sum(scenarios.values())
    for scen, count in scenarios.most_common():
        pct = (count/total)*100
        bar = "█" * int(pct/2)
        print(f"  {scen:15} {count:4} ({pct:5.1f}%) {bar}")
    
    # Detectar si hay demasiados "ayuda"
    ayuda_pct = (scenarios.get('ayuda', 0) / total) * 100
    if ayuda_pct > 30:
        print(f"\n⚠️  ALERTA: {ayuda_pct:.1f}% de mensajes van a 'ayuda'")
        print("   Esto sugiere que el bot no entiende bien las consultas.")


def analyze_conversation_flow(logs):
    """Analiza flujos de conversación"""
    print("\n" + "="*80)
    print("🔄 ANÁLISIS DE FLUJOS DE CONVERSACIÓN")
    print("="*80)
    
    # Agrupar por sesiones (aproximado: por ventana de 30 min)
    sessions = []
    current_session = []
    last_time = None
    
    for log in logs:
        timestamp = datetime.fromisoformat(log['timestamp'])
        
        if last_time and (timestamp - last_time).seconds > 1800:  # 30 min
            if current_session:
                sessions.append(current_session)
            current_session = []
        
        current_session.append(log)
        last_time = timestamp
    
    if current_session:
        sessions.append(current_session)
    
    print(f"\n📝 Se detectaron {len(sessions)} sesiones de conversación")
    
    # Analizar sesiones largas con problemas
    problematic = []
    for session in sessions:
        if len(session) >= 3:
            # Ver si se queda atascado en un escenario
            scenarios_in_session = [log['scenario'] for log in session]
            if scenarios_in_session.count('ayuda') >= len(session) * 0.6:
                problematic.append({
                    'start': session[0]['timestamp'],
                    'length': len(session),
                    'messages': [log['user'][:50] for log in session[:3]]
                })
    
    if problematic:
        print(f"\n⚠️  {len(problematic)} sesiones problemáticas (usuarios atascados):\n")
        for i, sess in enumerate(problematic[:5], 1):
            print(f"{i}. [{sess['start'][:16]}] - {sess['length']} mensajes")
            print(f"   Mensajes: {sess['messages']}")
            print()


def find_common_failures(logs):
    """Encuentra los errores más comunes"""
    print("\n" + "="*80)
    print("🐛 ERRORES MÁS COMUNES")
    print("="*80)
    
    # Buscar mensajes repetidos que terminan en "ayuda"
    ayuda_messages = [log['user'] for log in logs if log['scenario'] == 'ayuda']
    common_ayuda = Counter(ayuda_messages).most_common(10)
    
    print("\n📌 Mensajes que más veces terminan en 'ayuda' (posibles errores):\n")
    for msg, count in common_ayuda:
        if count > 1:
            print(f"  {count}x: '{msg}'")


def generate_report(logs):
    """Genera reporte completo"""
    print("\n" + "="*80)
    print("📄 REPORTE GENERAL")
    print("="*80)
    
    total = len(logs)
    if total == 0:
        print("\n❌ No hay logs para analizar")
        return
    
    # Fechas
    dates = [datetime.fromisoformat(log['timestamp']) for log in logs]
    first_date = min(dates)
    last_date = max(dates)
    
    print(f"\n📅 Período analizado:")
    print(f"   Desde: {first_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Hasta: {last_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Total interacciones: {total}")
    
    # Hora pico
    hours = Counter(d.hour for d in dates)
    peak_hour = hours.most_common(1)[0][0]
    print(f"\n⏰ Hora pico de uso: {peak_hour}:00 hs")
    
    # Escenarios exitosos (no "ayuda")
    successful = sum(1 for log in logs if log['scenario'] != 'ayuda')
    success_rate = (successful / total) * 100
    
    print(f"\n✅ Tasa de éxito: {success_rate:.1f}%")
    print(f"   ({successful}/{total} consultas bien clasificadas)")
    
    if success_rate < 70:
        print("\n⚠️  RECOMENDACIÓN: La tasa de éxito es baja.")
        print("   Considera mejorar la detección de intenciones.")


def export_errors_json(misclassified, output="errors_report.json"):
    """Exporta errores a JSON para revisión"""
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(misclassified, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Reporte de errores guardado en: {output}")


def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🤖 ANÁLISIS DE LOGS - BOT FINANCIERO")
    print("="*80)
    
    csv_path = Path(__file__).parent / "chat_logs.csv"
    
    if not csv_path.exists():
        print(f"\n❌ No se encontró el archivo: {csv_path}")
        return
    
    # Cargar logs
    logs = load_logs(csv_path)
    print(f"\n✅ Cargados {len(logs)} registros de interacciones\n")
    
    # Análisis
    generate_report(logs)
    analyze_scenarios(logs)
    analyze_sentiment(logs)
    misclassified = analyze_misclassifications(logs)
    analyze_conversation_flow(logs)
    find_common_failures(logs)
    
    # Exportar errores
    if misclassified:
        export_errors_json(misclassified)
    
    print("\n" + "="*80)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*80)
    print("\n💡 Próximos pasos:")
    print("   1. Revisa los errores de clasificación más frecuentes")
    print("   2. Actualiza las keywords en chatbot_core.py")
    print("   3. Mejora la detección de contexto")
    print("   4. Testea con los casos problemáticos")
    print("\n")


if __name__ == "__main__":
    main()
