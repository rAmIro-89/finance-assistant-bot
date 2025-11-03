# test_complex_v2_4.py – Pruebas prolongadas y coloquiales para chatbot_core_v2.4

import requests
import json
import os
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")
session = requests.Session()

mensajes = [
    # Conversación prolongada (10+ turnos) mezclando ahorro e inversión
    "Che, cobro 350 lucas al mes, me conviene ahorrar o invertir?",
    "ponele que puedo guardar 100 lucas, qué hago?",
    "plazo fijo o FCI?",
    "y si lo dejo 3 meses?",
    "me conviene meter todo o ir de a poco?",
    "qué pasa si sube la inflación?",
    "y si necesito la guita antes?",
    "cuánto podría ganar más o menos?",
    "dame un ejemplo con 150 lucas.",
    "y después de eso, qué hago?",
    # Mensajes cortados / incompletos
    "plazo fijo 3 meses?",
    "fci?",
    "cer?",
    # Frases argentinas reales
    "la guita no me rinde nada",
    "vale la pena meter todo?",
    "me la morfo toda o la guardo?",
    # Temas educativos casuales
    "qué corno es inflación?",
    "explicame lo del interés compuesto"
]

resultados = []
print("\n🚀 Iniciando pruebas complejas versión v2.4 –", datetime.now().isoformat(), "\n")

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
with open("test_complex_v2_4_results.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("\n✅ Pruebas finalizadas. Resultados guardados en test_complex_v2_4_results.json\n")
