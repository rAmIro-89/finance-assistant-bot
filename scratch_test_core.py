from chatbot_core import ChatBot
from database import get_user, create_link_token, claim_link_token

print('--- scratch_test_core start ---')
# Test 1
bot = ChatBot()
bot.user_phone = 'test_user_wa'
res1 = bot.process('quiero invertir 150000 por 7 meses')
print('test1_scenario:', res1.scenario)
print('test1_has_horizonte:', 'Horizonte' in res1.reply or 'horizonte' in res1.reply)
res2 = bot.process('dale')
print('test1_confirm_scenario:', res2.scenario)
print('test1_confirm_has_interes:', any(s in res2.reply for s in ['Interés Compuesto','Interés compuesto','interés compuesto']))

# Test 2
bot2 = ChatBot()
uid = 'dni:12345679'
bot2.user_phone = uid
res = bot2.process('presupuesto con $50000')
user = get_user(uid)
print('test2_user_found:', user is not None)
print('test2_income:', user.monthly_income if user else None)

# Test 3
_tok = create_link_token('whatsapp:+111222333', ttl_minutes=1)
print('test3_token_created:', bool(_tok))
_claimed = claim_link_token(_tok)
print('test3_claimed:', _claimed)
print('test3_second_claim_none:', claim_link_token(_tok) is None)

print('--- scratch_test_core end ---')
