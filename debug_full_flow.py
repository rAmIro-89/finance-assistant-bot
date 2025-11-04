from chatbot_core import ChatBot
import re

def debug_full_flow():
    print("=== FULL FLOW DEBUG ===\n")
    
    bot = ChatBot()
    
    # Step 1: Set monto
    print("STEP 1: Set monto")
    res1 = bot.process("quiero invertir 150000")
    print(f"Context after step 1: {bot.conversation_state['partial_data']}")
    
    # Step 2: Set horizonte - debug internal processing
    print("\nSTEP 2: Set horizonte")
    text = "2 años"
    t = text.lower()
    
    # Manual parsing like in the function
    nums_raw = re.findall(r"\d+(?:[.,]\d+)?", text)
    nums = [float(n.replace('.', '').replace(',', '')) for n in nums_raw]
    tiene_ano = any(k in t for k in ["año", "años", "anio", "anios", "a."])
    
    horizonte_meses = None
    if tiene_ano:
        candidatos = [int(x) for x in nums if x <= 50]
        if candidatos:
            horizonte_meses = candidatos[0] * 12
    
    print(f"Manual parsing - horizonte_meses: {horizonte_meses}")
    
    # Get current context
    inv_ctx = bot.conversation_state['partial_data'].get('inversion', {})
    print(f"Current inv_ctx: {inv_ctx}")
    print(f"Has monto in context: {inv_ctx.get('monto')}")
    
    # Check condition for special logic
    condition = horizonte_meses is not None and inv_ctx.get('monto')
    print(f"Special logic condition: horizonte_meses={horizonte_meses}, has_monto={bool(inv_ctx.get('monto'))}, condition={condition}")
    
    # Execute step 2
    res2 = bot.process(text)
    print(f"Result scenario: {res2.scenario}")
    print(f"Result starts with: {res2.reply[:100]}...")
    print(f"Context after step 2: {bot.conversation_state['partial_data']}")

if __name__ == "__main__":
    debug_full_flow()