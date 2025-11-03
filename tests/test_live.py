import requests
import json
import os

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")

mensajes = [
    "Che loco, me pintó ponerme a ordenar la guita, cobro 450 lucas por mes, qué hago?",
    "Pará, igual tengo una deuda con la tarjeta del Galicia, ponele 200 lucas, qué hago primero?",
    "Y si pago el mínimo nomás, cuánto tardo más o menos?",
    "Okey, supongamos que la liquido en tres meses, después qué me conviene hacer con lo que me sobra?",
    "ponele que quiero meter 100 lucas, dónde rinde más?",
    "Tengo ganas de ahorrar para un auto pero no sé si conviene, viste los precios?",
    "Bueno, igual me fui al carajo, contame del interés compuesto",
    "Ajá, y si lo aplico a invertir mi aguinaldo?",
    "O sea que si pongo 200 lucas un año, cuánto saco más o menos?",
    "Ta bien, y otra, mi vieja quiere entender cómo hacer un presupuesto, le explicás?",
    "Qué onda, tengo 100 lucas tiradas, las meto en plazo fijo o algún fondo?",
    "Me conviene meter todo de una o ir de a poco?",
    "Y si la inflación sigue así, no es al pedo?",
    "Bueno dejá eso, me enseñás a hacer un presupuesto rápido?"
]

session = requests.Session()
resultados = []

try:
    # Sanity check del servidor
    r_debug = requests.get(f"{BASE_URL}/debug", timeout=6)
    print(f"🔍 Debug status: {r_debug.status_code}")
except Exception as e:
    print(f"❌ No se pudo conectar a {BASE_URL}/debug: {e}")

for m in mensajes:
    try:
        r = session.post(f"{BASE_URL}/api/chat", json={"message": m}, timeout=10)
        data = r.json() if r.status_code == 200 else {"error": f"HTTP {r.status_code}"}
        resultados.append({
            "user_msg": m,
            "status": r.status_code,
            "reply": data.get("reply", ""),
            "scenario": data.get("scenario", "")
        })
        print(f"👤 {m}\n🤖 ({r.status_code}) [{data.get('scenario','')}] {data.get('reply','[sin respuesta]')}\n")
    except Exception as e:
        resultados.append({"user_msg": m, "error": str(e)})
        print(f"❌ Error: {e}\n")

# Guardar resultados en archivo
with open("live_test_results.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)