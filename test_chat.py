from jarvis.services.llm_client import LLMClient

llm = LLMClient()

messages = [
    {"role": "system", "content": "You are Jarvis, a concise and smart AI assistant."},
    {"role": "user", "content": "Explain AI in one sentence."}
]

response = llm.chat(messages)

print(response)
