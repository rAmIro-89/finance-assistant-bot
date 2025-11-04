from chatbot_core import ChatBot
import sys

cases = [
    ("Presupuesto con $50000", "presupuesto"),
    ("Quiero ahorrar para un auto", "ahorro"),
    ("Invertir mi aguinaldo", "inversiones"),
    ("Tengo deuda de $30000", "deudas"),
    ("Qué es la inflación", "educacion"),
]

ok = True
bot = ChatBot()
for msg, expected in cases:
    res = bot.process(msg)
    got = res.scenario
    prefix = "✅" if got == expected else "❌"
    print(f"{prefix} {msg} -> {got} (expected {expected})\n   {res.reply[:160].replace(chr(10),' ')}\n")
    if got != expected:
        ok = False

# Context checks
bot2 = ChatBot()
res1 = bot2.process("Invertir mi aguinaldo")
res2 = bot2.process("dale")
if res2.scenario != "inversiones":
    ok = False
    print(f"❌ Context fail: expected inversiones after 'dale', got {res2.scenario}")
else:
    print("✅ Context ok for inversiones 'dale'")

bot3 = ChatBot()
res3 = bot3.process("Quiero ahorrar para un auto")
res4 = bot3.process("500000")
if res4.scenario != "ahorro":
    ok = False
    print(f"❌ Context fail: expected ahorro after amount, got {res4.scenario}")
else:
    print("✅ Context ok for ahorro after amount")

bot4 = ChatBot()
res5 = bot4.process("Presupuesto con $50000")
res6 = bot4.process("ok")
if res6.scenario != "presupuesto":
    ok = False
    print(f"❌ Context fail: expected presupuesto after ok, got {res6.scenario}")
else:
    print("✅ Context ok for presupuesto short confirm")

sys.exit(0 if ok else 1)
