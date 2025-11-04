from chatbot_core import ChatBot


def show(label: str, text: str, bot: ChatBot):
    res = bot.process(text)
    snippet = (res.reply or '').replace('\n', ' ')[:220]
    print(f"{label}: '{text}' -> scenario={res.scenario}\n  {snippet}\n")


def run_demo():
    print("-- EDUCACION (conceptos) --\n")
    edu_bot = ChatBot()
    for txt in [
        "que es inflacion",
        "tna",
        "cer?",
        "fci?",
        "etf?",
    ]:
        show("EDU", txt, edu_bot)

    print("-- INVERSIONES (instrumentos) --\n")
    inv_bot = ChatBot()
    show("INV", "cedear de apple", inv_bot)

    print("-- BONOS EN DOLARES: guia guiada (aceptación) --\n")
    usd_bot = ChatBot()
    show("USD", "dolares o pesos?", usd_bot)
    show("USD", "dale", usd_bot)

    print("-- BONOS EN DOLARES: pedido directo --\n")
    direct_bot = ChatBot()
    show("USD-DIRECTO", "como compro bonos en dolares", direct_bot)


if __name__ == "__main__":
    run_demo()
