# End-to-end topic variants against NAS API
import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://192.168.1.42:5000").rstrip("/")
sess = requests.Session()

MATRIX = {
    'presupuesto': [
        "presupuesto", "hacer presupuesto", "organizar gastos", "gano 120000", "cobro 350 lucas"
    ],
    'ahorro': [
        "quiero ahorrar", "necesito juntar plata", "quiero viajar a europa", "planear compra de auto", "alcancia"
    ],
    'inversiones': [
        "invertir mi aguinaldo", "donde rinde mas 200000", "tengo 100000 que hago", "cedear de apple"
    ],
    'deudas': [
        "tengo deuda de 300000", "no puedo pagar el prestamo", "tarjeta me cobra mucho"
    ],
    'educacion': [
        "que es inflacion", "que significa tna", "cer?", "fci?", "plazo fijo o fci?"
    ],
    'calculadora': [
        "calcular interes compuesto", "simular prestamo", "en cuanto tiempo pago 30000 si pago 5000 por mes"
    ],
}

for topic, phrases in MATRIX.items():
    for p in phrases:
        r = sess.post(f"{BASE_URL}/api/chat", json={"message": p}, timeout=12)
        data = r.json() if r.status_code == 200 else {}
        scenario = data.get('scenario', '?')
        reply = data.get('reply', '')
        mark = '✅' if scenario == topic else '❌'
        print(f"{mark} [{topic}] '{p}' -> {scenario}\n   {reply[:180].replace(chr(10),' ')}\n")

# Minimal flows
print("\n-- Flows --\n")
# Presupuesto
sess.post(f"{BASE_URL}/api/chat", json={"message": "hacer presupuesto"})
r = sess.post(f"{BASE_URL}/api/chat", json={"message": "120000"}); print('P2:', r.json().get('scenario'))
# Ahorro
sess.post(f"{BASE_URL}/api/chat", json={"message": "quiero ahorrar"})
r = sess.post(f"{BASE_URL}/api/chat", json={"message": "auto"}); print('A2:', r.json().get('scenario'))
r = sess.post(f"{BASE_URL}/api/chat", json={"message": "300000"}); print('A3:', r.json().get('scenario'))
# Inversiones
sess.post(f"{BASE_URL}/api/chat", json={"message": "quiero invertir 150000 por 7 meses"})
r = sess.post(f"{BASE_URL}/api/chat", json={"message": "dale, 5000 de ahorro mensual y tasa del 15%"}); print('I2:', r.json().get('scenario'))
# Dólar → explicar bonos USD
sess.post(f"{BASE_URL}/api/chat", json={"message": "dolares o pesos argentinos"})
r = sess.post(f"{BASE_URL}/api/chat", json={"message": "dale"}); print('D2:', r.json().get('scenario'))
