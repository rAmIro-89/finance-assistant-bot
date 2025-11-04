from chatbot_core import ChatBot

# Reproduce the misclassification case and verify it's fixed
bot = ChatBot()
# Provide inversiones data first
print('> User: 1000, 2 años')
res1 = bot.process('1000, 2 años')  # should not alone set inversiones; but to ensure inversiones context, say:
if res1.scenario != 'inversiones':
    # Seed inversiones context properly
    bot = ChatBot()
    print('> Seed inversiones: Quiero invertir 1000 por 2 años')
    res1 = bot.process('Quiero invertir 1000 por 2 años')
print(f"<- ({res1.scenario}) {res1.reply[:160].replace('\n',' ')}\n")

# Now confirm simulation with tasa and aporte using the word 'ahorro mensual'
print('> User: dale, 5000 de ahorro mensual y tasa del 35%')
res2 = bot.process('dale, 5000 de ahorro mensual y tasa del 35%')
print(f"<- ({res2.scenario}) {res2.reply[:280].replace('\n',' ')}\n")

ok = res2.scenario == 'inversiones' and ('Simulación' in res2.reply or 'Simul' in res2.reply)
print('RESULT:', '✅ Fixed' if ok else '❌ Still wrong')
