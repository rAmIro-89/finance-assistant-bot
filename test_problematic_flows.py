from chatbot_core import ChatBot


def test_problematic_flows():
    print("=== PROBLEMAS IDENTIFICADOS ===\n")
    
    print("1. EDUCACION: FCI/conceptos específicos")
    print("-" * 50)
    edu_bot = ChatBot()
    
    # Test del screenshot: "que es un FCI?"
    res = edu_bot.process("que es un FCI?")
    print(f"Input: 'que es un FCI?'")
    print(f"Scenario: {res.scenario}")
    print(f"Reply: {res.reply[:200]}...\n")
    
    # Test: conceptos prometidos en el menú
    concepts = ["interes simple vs compuesto", "diversificacion", "oro como inversion"]
    for concept in concepts:
        edu_bot2 = ChatBot()
        res = edu_bot2.process(concept)
        print(f"Input: '{concept}'")
        print(f"Scenario: {res.scenario}")
        print(f"Reply: {res.reply[:150]}...\n")
    
    print("\n2. INVERSIONES: Simulación de bonos prometida pero no implementada")
    print("-" * 70)
    bonds_bot = ChatBot()
    res1 = bonds_bot.process("como compro bonos en dolares")
    print(f"Step 1: 'como compro bonos en dolares' -> {res1.scenario}")
    print(f"Reply ends with: {res1.reply[-100:]}\n")
    
    res2 = bonds_bot.process("si")
    print(f"Step 2: 'si' (para simular bonos)")
    print(f"Scenario: {res2.scenario}")
    print(f"Reply: {res2.reply[:200]}...\n")
    
    print("\n3. INVERSIONES: Preguntas sobre plazo que no se procesan bien")
    print("-" * 65)
    time_bot = ChatBot()
    res1 = time_bot.process("quiero invertir 100000")
    print(f"Step 1: 'quiero invertir 100000' -> {res1.scenario}")
    print(f"Reply ends with: {res1.reply[-80:]}\n")
    
    res2 = time_bot.process("2 años")
    print(f"Step 2: '2 años'")
    print(f"Scenario: {res2.scenario}")
    print(f"Reply: {res2.reply[:200]}...\n")


if __name__ == "__main__":
    test_problematic_flows()