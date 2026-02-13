# jarvis/voice/listener.py
class Listener:
    def listen(self) -> str:
        try:
            return input("Tu: ")
        except EOFError:
            return ""
