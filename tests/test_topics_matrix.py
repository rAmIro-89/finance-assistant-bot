from chatbot_core import ChatBot

# Variantes por tópico (detección)
DETECTION_CASES = [
    # Presupuesto
    ("presupuesto", "presupuesto"),
    ("hacer presupuesto", "presupuesto"),
    ("organizar gastos", "presupuesto"),
    ("gano 120000", "presupuesto"),
    ("cobro 350 lucas", "presupuesto"),
    # Ahorro
    ("quiero ahorrar", "ahorro"),
    ("necesito juntar plata", "ahorro"),
    ("quiero viajar a europa", "ahorro"),
    ("planear compra de auto", "ahorro"),
    ("alcancia", "ahorro"),
    # Inversiones
    ("invertir mi aguinaldo", "inversiones"),
    ("donde rinde mas 200000", "inversiones"),
    ("tengo 100000 que hago", "inversiones"),
    ("plazo fijo o fci?", "educacion"),
    ("cedear de apple", "inversiones"),
    # Deudas
    ("tengo deuda de 300000", "deudas"),
    ("no puedo pagar el prestamo", "deudas"),
    ("tarjeta me cobra mucho", "deudas"),
    # Educación
    ("que es inflacion", "educacion"),
    ("que significa tna", "educacion"),
    ("cer?", "educacion"),
    ("fci?", "educacion"),
    # Calculadora
    ("calcular interes compuesto", "calculadora"),
    ("simular prestamo", "calculadora"),
    ("en cuanto tiempo pago 30000 si pago 5000 por mes", "calculadora"),
]


def test_detection_variants_table():
    for msg, expected in DETECTION_CASES:
        bot = ChatBot()
        res = bot.process(msg)
        assert res.scenario == expected, f"'{msg}' → esperado {expected}, obtuvo {res.scenario}"


def test_presupuesto_flow_with_amount_and_short_confirm():
    bot = ChatBot()
    r1 = bot.process("hacer presupuesto")
    assert r1.scenario == "presupuesto"
    r2 = bot.process("120000")
    assert r2.scenario == "presupuesto"
    r3 = bot.process("ok")
    assert r3.scenario == "presupuesto"


def test_ahorro_flow_meta_monto_plazo_and_guard_against_aporte_confusion():
    bot = ChatBot()
    r1 = bot.process("quiero ahorrar")
    assert r1.scenario == "ahorro"
    r2 = bot.process("auto")
    assert r2.scenario == "ahorro"
    r3 = bot.process("300000")
    assert r3.scenario == "ahorro"
    # No debería interpretar '5000 mensual' como '5000 meses'
    r4 = bot.process("5000 ahorro mensual")
    # A falta de plazo válido, debería pedir explícitamente el tiempo o mantener ahorro
    assert r4.scenario == "ahorro"


def test_inversiones_flow_with_monto_plazo_then_simular_and_aporte_tasa():
    bot = ChatBot()
    r1 = bot.process("quiero invertir 150000 por 7 meses")
    assert r1.scenario == "inversiones"
    # Confirmación y parámetros de simulación
    r2 = bot.process("dale, 5000 de ahorro mensual y tasa del 15%")
    assert r2.scenario == "inversiones"
    assert ("Simul" in r2.reply) or ("interés" in r2.reply.lower())


def test_inversiones_dolar_then_explain_bonos_usd():
    bot = ChatBot()
    r1 = bot.process("dolares o pesos argentinos")
    assert r1.scenario == "inversiones"
    r2 = bot.process("dale")
    assert r2.scenario == "inversiones"
    assert ("bonos en dólares" in r2.reply) or ("bonos en dolares" in r2.reply.lower())


def test_deudas_flow_deuda_then_pago_mensual():
    bot = ChatBot()
    r1 = bot.process("tengo una deuda de 120000")
    assert r1.scenario == "deudas"
    r2 = bot.process("pago 10000 por mes")
    assert r2.scenario == "deudas"
    assert ("Liquidarás" in r2.reply) or ("Liquidaras" in r2.reply)


def test_educacion_acronyms_and_concepts():
    bot = ChatBot()
    for msg in ["cer?", "tna", "etf?", "que es inflacion", "como funciona el plazo fijo"]:
        r = bot.process(msg)
        assert r.scenario == "educacion", f"'{msg}' debería ser educación"


def test_calculadora_interest_and_loan():
    bot = ChatBot()
    r1 = bot.process("cuanto ganaria si invierto 100000 por 5 años al 12%")
    assert r1.scenario == "calculadora"
    assert ("Simulación" in r1.reply) or ("RESULTADO" in r1.reply)
    r2 = bot.process("cuota de prestamo 50000 a 12 meses 50%")
    assert r2.scenario == "calculadora"
    assert ("Cuota mensual" in r2.reply) or ("Simulación de Préstamo" in r2.reply)


def test_slang_lucas_and_travel_mapping():
    bot = ChatBot()
    r1 = bot.process("cobro 300 lucas")
    assert r1.scenario == "presupuesto"
    r2 = bot.process("quiero viajar a japon")
    assert r2.scenario == "ahorro"
