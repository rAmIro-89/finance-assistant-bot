from chatbot_core import ChatBot


def test_direct():
    bot = ChatBot()
    
    # Set up context manually
    bot.conversation_state['partial_data'] = {
        'inversion': {'monto': 150000.0, 'horizonte_meses': None}
    }
    
    print("Context setup:", bot.conversation_state['partial_data'])
    
    # Test the timeline input
    result = bot.handle_inversiones("2 años", None)
    print("Result:", result[:200])


if __name__ == "__main__":
    test_direct()