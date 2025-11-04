from chatbot_core import ChatBot


def test_explain_bonos_usd_after_dolar_question():
    bot = ChatBot()
    # Usuario pregunta dólares vs pesos → bot menciona USD y ofrece explicar bonos en dólares
    r1 = bot.process('dolares o pesos argentinos')
    assert r1.scenario == 'inversiones'
    # Acepta explicación
    r2 = bot.process('dale')
    assert r2.scenario == 'inversiones'
    assert ('Cómo comprar bonos en dólares' in r2.reply) or ('bonos en dólares' in r2.reply)


def test_direct_explain_bonos_usd_phrase():
    bot = ChatBot()
    r = bot.process('quiero que me expliques como comprar bonos en dolares')
    assert r.scenario == 'inversiones'
    assert ('Cómo comprar bonos en dólares' in r.reply) or ('bonos en dólares' in r.reply)
