# Quick NAS test for the welcome suggested prompts
import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")
session = requests.Session()

cases = [
    ("Presupuesto con $50000", "presupuesto"),
    ("Quiero ahorrar para un auto", "ahorro"),
    ("Invertir mi aguinaldo", "inversiones"),
    ("Tengo deuda de $30000", "deudas"),
    ("Qué es la inflación", "educacion"),
]

for msg, expected in cases:
    r = session.post(f"{BASE_URL}/api/chat", json={"message": msg}, timeout=10)
    try:
        data = r.json()
    except Exception:
        data = {}
    scenario = data.get("scenario", "?")
    reply = data.get("reply", "")
    ok = "✅" if scenario == expected else "❌"
    print(f"{ok} {msg} -> {scenario} (expected {expected})\n   {reply[:160].replace(chr(10),' ')}\n")
