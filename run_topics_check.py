from chatbot_core import ChatBot

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

def check_detection():
    total = 0
    ok = 0
    for topic, phrases in MATRIX.items():
        for p in phrases:
            bot = ChatBot()
            res = bot.process(p)
            total += 1
            hit = res.scenario == topic
            if hit:
                ok += 1
            mark = '✅' if hit else '❌'
            print(f"{mark} [{topic}] '{p}' -> {res.scenario}")
    print(f"\nDetection: {ok}/{total} correct")


def check_flows():
    print("\n-- Flows --")
    # Presupuesto
    bot = ChatBot()
    res = bot.process("hacer presupuesto"); print('P1:', res.scenario)
    res = bot.process("120000"); print('P2:', res.scenario)
    res = bot.process("ok"); print('P3:', res.scenario)

    # Ahorro
    bot = ChatBot()
    res = bot.process("quiero ahorrar"); print('A1:', res.scenario)
    res = bot.process("auto"); print('A2:', res.scenario)
    res = bot.process("300000"); print('A3:', res.scenario)
    res = bot.process("5000 ahorro mensual"); print('A4:', res.scenario)

    # Inversiones
    bot = ChatBot()
    res = bot.process("quiero invertir 150000 por 7 meses"); print('I1:', res.scenario)
    res = bot.process("dale, 5000 de ahorro mensual y tasa del 15%"); print('I2:', res.scenario)

    # Dólar → explicar bonos USD
    bot = ChatBot()
    res = bot.process("dolares o pesos argentinos"); print('D1:', res.scenario)
    res = bot.process("dale"); print('D2:', res.scenario)

    # Deudas
    bot = ChatBot()
    res = bot.process("tengo una deuda de 120000"); print('DE1:', res.scenario)
    res = bot.process("pago 10000 por mes"); print('DE2:', res.scenario)

    # Educación
    bot = ChatBot()
    for p in ["cer?", "tna", "etf?", "que es inflacion"]:
        res = bot.process(p); print('ED:', p, '->', res.scenario)

    # Calculadora
    bot = ChatBot()
    res = bot.process("cuanto ganaria si invierto 100000 por 5 años al 12%"); print('C1:', res.scenario)
    res = bot.process("cuota de prestamo 50000 a 12 meses 50%"); print('C2:', res.scenario)


if __name__ == '__main__':
    check_detection()
    check_flows()
