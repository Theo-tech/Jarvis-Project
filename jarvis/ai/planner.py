import json
from typing import List
from jarvis.core.action import Action
from jarvis.services.llm_client import LLMClient


class Planner:

    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_input: str) -> List[Action]:
        prompt = f"""
        You are an AI assistant planner.

        Convert the user request into a JSON list of actions.

        Available actions:
        - open_app(name: str)
        - web_search(query: str)

        Respond ONLY with valid JSON.

        User request:
        {user_input}
        """

        response = self.llm.generate(prompt)

        try:
            parsed = json.loads(response)
            return [Action(**item) for item in parsed]
        except Exception as e:
            print("Planner parsing error:", e)
            return []
