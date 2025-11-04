from chatbot_core import ChatBot


def test_debug_bonos():
    print("=== DEBUG BONOS USD SIMULATION ===\n")
    
    bonos_bot = ChatBot()
    
    # Paso 1: pregunta sobre dólares - debe setear waiting_for
    res1 = bonos_bot.process("dolares o pesos?")
    print(f"Step 1: waiting_for = {bonos_bot.conversation_state.get('waiting_for')}")
    
    # Paso 2: dale - debe mostrar guía y resetear waiting_for
    res2 = bonos_bot.process("dale")
    print(f"Step 2: waiting_for = {bonos_bot.conversation_state.get('waiting_for')}")
    
    # Paso 3: simular debe detectar like "si" y números, y tener waiting_for=None
    text_step3 = "si, simular 50000 por 3 años"
    t = text_step3.lower()
    print(f"Step 3 input: '{text_step3}'")
    print(f"Step 3 normalized: '{t}'")
    print(f"Step 3 waiting_for: {bonos_bot.conversation_state.get('waiting_for')}")
    print(f"Step 3 'si' in t: {'si' in t}")
    print(f"Step 3 numbers found: {[x for x in t.split() if any(c.isdigit() for c in x)]}")
    
    # Ejecutar el step 3
    res3 = bonos_bot.process(text_step3)
    print(f"Step 3 result scenario: {res3.scenario}")
    print(f"Step 3 reply preview: {res3.reply[:200]}...")


def test_debug_plazo():
    print("\n=== DEBUG PLAZO PROCESSING ===\n")
    
    plazo_bot = ChatBot()
    
    # Paso 1: dar monto
    res1 = plazo_bot.process("quiero invertir 150000")
    print(f"Step 1 context: {plazo_bot.conversation_state['partial_data']}")
    
    # Paso 2: dar plazo - debe disparar lógica especial
    text_step2 = "2 años"
    print(f"Step 2 input: '{text_step2}'")
    
    # Ver si detecta el contexto previo correctamente
    inv_ctx = plazo_bot.conversation_state['partial_data'].get('inversion', {})
    print(f"Step 2 inv_ctx: {inv_ctx}")
    print(f"Step 2 has monto?: {inv_ctx.get('monto')}")
    
    res2 = plazo_bot.process(text_step2)
    print(f"Step 2 scenario: {res2.scenario}")
    print(f"Step 2 reply preview: {res2.reply[:200]}...")


if __name__ == "__main__":
    test_debug_bonos()
    test_debug_plazo()