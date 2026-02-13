# scripts/run_assistant.py
from jarvis.core.assistant import Assistant

def main():
    assistant = Assistant(debug=True)
    print("Assistant démarré — ctrl+C pour quitter.")
    try:
        while True:
            text = input("Tu : ")
            if not text:
                continue
            print("Jarvis :", assistant.handle(text))
    except (KeyboardInterrupt, EOFError):
        print("\nÀ bientôt.")

if __name__ == "__main__":
    main()
