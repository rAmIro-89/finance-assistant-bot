from chatbot_core import ChatBot


def test_inversiones_simulation_with_aporte_and_tasa_keeps_context():
    bot = ChatBot()
    r1 = bot.process('Quiero invertir 1000 por 2 años')
    assert r1.scenario == 'inversiones'
    r2 = bot.process('dale, 5000 de ahorro mensual y tasa del 35%')
    assert r2.scenario == 'inversiones'
    assert ('Simulación' in r2.reply) or ('Simul' in r2.reply) or ('interés compuesto' in r2.reply.lower())
    assert '35' in r2.reply or '35%' in r2.reply
    assert '5,000' in r2.reply or '5000' in r2.reply
