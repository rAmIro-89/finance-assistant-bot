from chatbot_core import ChatBot


def test_suggested_prompts_cover_expected_scenarios():
    bot = ChatBot()
    cases = [
        ("Presupuesto con $50000", "presupuesto"),
        ("Quiero ahorrar para un auto", "ahorro"),
        ("Invertir mi aguinaldo", "inversiones"),
        ("Tengo deuda de $30000", "deudas"),
        ("Qué es la inflación", "educacion"),
    ]
    for msg, expected in cases:
        res = bot.process(msg)
        assert res.scenario == expected, f"For '{msg}' expected {expected} got {res.scenario}. Reply: {res.reply[:120]}"


def test_short_confirmations_keep_context_for_suggested_paths():
    bot = ChatBot()
    # Start with inversiones, then short confirmation should keep scenario
    res1 = bot.process("Invertir mi aguinaldo")
    assert res1.scenario == "inversiones"
    res2 = bot.process("dale")
    assert res2.scenario == "inversiones"
    # Presupuesto with amount, then short confirm should keep presupuesto
    bot3 = ChatBot()
    res5 = bot3.process("Presupuesto con $50000")
    assert res5.scenario == "presupuesto"
    res6 = bot3.process("ok")
    assert res6.scenario == "presupuesto"
    # Start with ahorro target, short numeric reply should keep ahorro
    bot2 = ChatBot()
    res3 = bot2.process("Quiero ahorrar para un auto")
    assert res3.scenario == "ahorro"
    res4 = bot2.process("500000")
    assert res4.scenario == "ahorro"
