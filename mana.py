from buddhi import think, warmup


class Mana:
    def __init__(self):
        pass

    def process(self, user_input: str):
        print("You said:", user_input)
        print("//Thinking . . .")

        result = think(user_input)

        return result


def warmup_system():
    print("//...Warming up the brain")
    warmup()


# --- Voice Runner ---

def run_voice_mode():
    from ears import listen, get_model
    from mouth import speak

    print("//...Starting Voice Mode")
    get_model()          # warm up Whisper
    warmup_system()      # warm up LLM

    mana = Mana()

    while True:
        user_input = listen()
        result = mana.process(user_input)

        if isinstance(result, tuple):
            speak(result[0])
            if result[1] == "exit":
                break
        else:
            speak(result)


if __name__ == "__main__":
    run_voice_mode()