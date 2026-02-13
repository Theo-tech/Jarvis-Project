import requests

class LLMClient:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"
        self.history = [
            {
                "role": "system",
                "content": "You are Jarvis, a smart, concise and helpful AI assistant."
            }
        ]

    def chat(self, user_input):
        # Ajouter le message utilisateur
        self.history.append({
            "role": "user",
            "content": user_input
        })

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": self.history,
                "stream": False
            }
        )

        assistant_message = response.json()["message"]["content"]

        # Ajouter réponse assistant à l’historique
        self.history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message
