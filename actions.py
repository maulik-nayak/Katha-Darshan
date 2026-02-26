import webbrowser
from datetime import datetime

def handle_action(user_input):
    user_input = user_input.lower()

    if "open youtube" in user_input:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    if "time" in user_input:
        return f"The time is {datetime.now().strftime('%H:%M')}"

    if "stop" in user_input:
        return "Shutting down.", "exit"

    return None