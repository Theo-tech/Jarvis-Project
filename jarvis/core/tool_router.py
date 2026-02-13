# jarvis/core/tool_router.py
from typing import Any, Callable, Dict, Optional

class ToolRouter:
    """
    Router simple : on enregistre des handlers par nom d'intent,
    puis on appelle execute(intent, raw_text).
    Handler signature attendue : handler(intent: dict, raw_text: str) -> Union[str, dict]
    """
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable):
        self.tools[name] = handler

    def execute(self, intent: dict, raw_text: Optional[str] = None) -> Any:
        name = intent.get("name")
        if not name:
            raise KeyError("Intent sans champ 'name'")
        handler = self.tools.get(name)
        if handler is None:
            raise KeyError(f"Aucun handler enregistré pour l'intent '{name}'")
        # appel du handler : on fournit intent et raw_text (handler peut ignorer raw_text)
        return handler(intent, raw_text)
