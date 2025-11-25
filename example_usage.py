"""
Example usage of the Financial Assistant Chatbot.

This script demonstrates:
1. Starting the Flask web server
2. Making API calls to the chatbot
3. Accessing the dashboard
4. Testing core functionality
"""

import requests
import json
from time import sleep


def main():
    """Main demonstration function."""
    
    print("=" * 70)
    print("FINANCIAL ASSISTANT CHATBOT - DEMO")
    print("=" * 70)
    
    base_url = "http://localhost:5000"
    
    # Step 1: Check health
    print("\n[1/4] Checking server health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("  ✓ Server is running")
        else:
            print("  ✗ Server not responding. Please start the server:")
            print("     python web_app.py")
            return
    except requests.exceptions.ConnectionError:
        print("  ✗ Cannot connect to server. Please start it:")
        print("     python web_app.py")
        return
    
    # Step 2: Send chat message
    print("\n[2/4] Sending chat message...")
    chat_payload = {
        "message": "Quiero hacer un presupuesto"
    }
    
    response = requests.post(
        f"{base_url}/api/chat",
        json=chat_payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"  Bot response: {data.get('response', 'No response')[:100]}...")
    else:
        print(f"  ✗ Error: {response.status_code}")
    
    # Step 3: Access dashboard
    print("\n[3/4] Dashboard Access...")
    print(f"  Open in browser: {base_url}/dashboard")
    print("  Features:")
    print("  - 50/30/20 Budget Rule visualization")
    print("  - Compound interest calculator")
    print("  - Investment comparison charts")
    print("  - Debt payoff analyzer")
    
    # Step 4: WhatsApp integration info
    print("\n[4/4] WhatsApp Integration...")
    print("  To enable WhatsApp:")
    print("  1. Configure Twilio webhook: https://YOUR_DOMAIN/whatsapp-webhook")
    print("  2. Send 'vincular' via WhatsApp")
    print("  3. Open the secure link to connect WhatsApp → Web")
    
    # Summary
    print("\n" + "=" * 70)
    print("AVAILABLE INTENTS")
    print("=" * 70)
    print("""
1. Budget Planning: "Quiero hacer un presupuesto", "50/30/20"
2. Savings: "Quiero ahorrar", "objetivo de ahorro"
3. Investments: "Quiero invertir", "comparar inversiones"
4. Debt Management: "Tengo deudas", "refinanciar préstamo"
5. Calculators: "interés compuesto", "calcular cuota"
6. Education: "Qué es un plazo fijo", "explicame los bonos"
    """)
    
    print("\n" + "=" * 70)
    print("TESTING")
    print("=" * 70)
    print("\nRun comprehensive tests:")
    print("  pytest -v")
    print("\nGenerate test report:")
    print("  python generate_test_report.py")
    
    print("\n" + "=" * 70)
    print("DOCKER DEPLOYMENT")
    print("=" * 70)
    print("\nDeploy with Docker Compose:")
    print("  docker-compose up -d")
    print("\nView logs:")
    print("  docker-compose logs -f")
    print("\nStop containers:")
    print("  docker-compose down")
    
    print("\n✓ Demo complete! Server is ready for use.")


if __name__ == "__main__":
    main()
