from jarvis.services.llm_client import LLMClient

llm = LLMClient()
print(llm.generate("Say hello in one word"))