"""
Entry point for Jarvis.
No business logic here.
"""

from jarvis.services.llm_client import LLMClient


def run():
    llm = LLMClient()

    print("Bonjour monsieur, à votre service\n")

    while True:
        user_input = input("Vous > ")

        if user_input.lower() in ["exit", "quit"]:
            print("Jarvis > À bientôt.")
            break

        response = llm.chat(user_input)

        print(f"Jarvis > {response}\n")


if __name__ == "__main__":
    run()
