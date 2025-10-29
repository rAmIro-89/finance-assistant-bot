import re
from chatbot_core import ChatBot
from database import get_user, create_link_token, claim_link_token


def test_inversiones_dale_flow():
    bot = ChatBot()
    bot.user_phone = 'test_user_wa'
    # Usuario define monto y horizonte
    res1 = bot.process('quiero invertir 150000 por 7 meses')
    assert res1.scenario == 'inversiones'
    assert 'Horizonte' in res1.reply
    # Confirmación corta
    res2 = bot.process('dale')
    assert res2.scenario == 'inversiones'
    assert 'Interés Compuesto' in res2.reply or 'Interés compuesto' in res2.reply or 'interés compuesto' in res2.reply


def test_presupuesto_persist_monthly_income():
    bot = ChatBot()
    uid = 'dni:12345679'
    bot.user_phone = uid
    res = bot.process('presupuesto con $50000')
    user = get_user(uid)
    assert user is not None
    assert user.monthly_income == 50000


def test_link_token_create_and_claim():
    tok = create_link_token('whatsapp:+111222333', ttl_minutes=1)
    assert tok
    claimed = claim_link_token(tok)
    assert claimed == 'whatsapp:+111222333'
    # Segundo claim debe fallar
    assert claim_link_token(tok) is None
