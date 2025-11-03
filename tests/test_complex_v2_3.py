# test_complex_v2_3.py – Pruebas de conversación compleja para chatbot_core_v2.3

import requests
import json
import os
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")
session = requests.Session()

mensajes = [
    # Conversaciones con contexto de arrastre
    "Che, pagué la tarjeta al final.",
    "Y ahora me sobran 100 lucas, qué puedo hacer?",
    "Bah, capaz que ahorro un poco.",
    # Preguntas ambiguas y coloquiales
    "Me conviene meter la guita en algo o guardarla?",
    "Qué hago con el aguinaldo?",
    "Ponele que me rinde 10%... eso es bueno?",
    # Magnitudes y cálculos
    "Cobro 300 lucas por mes, cuánto debería ahorrar?",
    "Tengo 200 lucas en plazo fijo, cuánto gano en 3 meses?",
    # Cierre y reenganche educativo
    "Bueno, cambiando de tema... qué es la inflación?",
    "Ah, joya. Y cómo se calcula eso del interés compuesto?"
]

resultados = []
print("\n🚀 Iniciando pruebas complejas contra el bot (v2.3) –", datetime.now().isoformat(), "\n")

try:
    rd = requests.get(f"{BASE_URL}/debug", timeout=6)
    print(f"🔍 Debug status: {rd.status_code}")
except Exception as e:
    print(f"❌ No se pudo conectar a {BASE_URL}/debug: {e}")

for i, msg in enumerate(mensajes, start=1):
    try:
        r = session.post(f"{BASE_URL}/api/chat", json={"message": msg}, timeout=12)
        data = r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}"}
        resultados.append({
            "turn": i,
            "user_msg": msg,
            "status": r.status_code,
            "reply": data.get("reply", ""),
            "scenario": data.get("scenario", ""),
            "timestamp": data.get("timestamp", "")
        })
        print(f"{i:02d}. 👤 {msg}\n   🤖 ({data.get('scenario','?')}) {data.get('reply','[sin respuesta]')[:220]}\n")
    except Exception as e:
        resultados.append({"turn": i, "user_msg": msg, "error": str(e)})
        print(f"❌ Error en turno {i}: {e}\n")

# Guardar resultados
with open("test_complex_v2_3_results.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("\n✅ Pruebas finalizadas. Resultados guardados en test_complex_v2_3_results.json\n")
