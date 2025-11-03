# test_complex_v2_5.py – Pruebas realistas con lenguaje argentino para chatbot_core_v2.5

import requests
import json
import os
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")
session = requests.Session()

mensajes = [
    # Inicio de conversación – mezcla de temas
    "Che, cobro 400 lucas por mes, me conviene invertir o guardar?",
    "mirá, tengo una deuda chica de la tarjeta, la pago o la estiro?",
    "y si me sobra algo después?",
    "ponele que son 150 lucas, qué hago?",
    "plazo fijo, FCI o UVA?",
    "posta que el plazo fijo no sirve más?",
    # Cambios de tema y expresiones naturales
    "re conviene meter en bonos cer?",
    "y si lo hago de a poco, tipo todos los meses?",
    "me quedó guita de las vacaciones, qué hago?",
    "vale la pena meter todo junto?",
    # Frases cortas y ambiguas
    "cer?",
    "fci?",
    "ni idea qué es eso del interés compuesto",
    "qué corno es inflación?",
    "y eso cómo me afecta a mí?",
    "okey, y si quiero arrancar tranqui?",
    # Frases coloquiales y modismos
    "me la morfo toda o la guardo?",
    "no me rinde nada la guita",
    "cómo hago para que me rinda posta?",
    "dame un ejemplo con 200 lucas a 3 meses"
]

resultados = []
print("\n🚀 Iniciando pruebas de chatbot v2.5 –", datetime.now().isoformat(), "\n")

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
with open("test_complex_v2_5_results.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("\n✅ Pruebas finalizadas. Resultados guardados en test_complex_v2_5_results.json\n")
