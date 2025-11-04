from chatbot_core import ChatBot


def test_specific_fixes():
    print("=== TESTS ESPECÍFICOS CORREGIDOS ===\n")
    
    print("1. BONOS USD: Flujo completo dale->simulacion")
    print("-" * 50)
    bonos_bot = ChatBot()
    res1 = bonos_bot.process("dolares o pesos?")
    print(f"Step 1: 'dolares o pesos?' -> {res1.scenario}")
    print(f"Waiting for: {bonos_bot.conversation_state.get('waiting_for')}")
    print(f"Reply ends with: {res1.reply[-60:]}\n")
    
    res2 = bonos_bot.process("dale")
    print(f"Step 2: 'dale' (acepta explicar bonos)")
    print(f"Scenario: {res2.scenario}")
    print(f"Waiting for: {bonos_bot.conversation_state.get('waiting_for')}")
    print(f"Reply ends with: {res2.reply[-80:]}\n")
    
    res3 = bonos_bot.process("si, simular 50000 por 3 años")
    print(f"Step 3: 'si, simular 50000 por 3 años'")
    print(f"Scenario: {res3.scenario}")
    print(f"Reply starts with: {res3.reply[:100]}...\n")
    
    print("\n2. INVERSIONES: Plazo tras monto")
    print("-" * 40)
    plazo_bot = ChatBot()
    res1 = plazo_bot.process("quiero invertir 150000")
    print(f"Step 1: 'quiero invertir 150000' -> {res1.scenario}")
    print(f"Context: {plazo_bot.conversation_state['partial_data']}")
    print(f"Reply ends with: {res1.reply[-50:]}\n")
    
    res2 = plazo_bot.process("2 años")
    print(f"Step 2: '2 años'")
    print(f"Scenario: {res2.scenario}")
    print(f"Context: {plazo_bot.conversation_state['partial_data']}")
    print(f"Reply starts with: {res2.reply[:150]}...\n")


if __name__ == "__main__":
    test_specific_fixes()