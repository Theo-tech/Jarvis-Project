# jarvis/core/assistant.py
import re
from typing import Optional

try:
    from .intent_engine import IntentEngine
except Exception:
    IntentEngine = None  # fallback si tu n'as pas ce module

from .tool_router import ToolRouter

class Assistant:
    """
    Assistant central : parse un texte en intent, appelle le router et renvoie la réponse.
    """
    def __init__(self, router: Optional[ToolRouter] = None, tts=None):
        self.intent_engine = IntentEngine() if IntentEngine is not None else None
        self.tool_router = router or ToolRouter()
        self.tts = tts

    def parse_intent_local(self, text: str):
        """
        Parseur local minimal pour les commandes du type:
          ouvre|ouvrir|lance|lancer <nom_app>
        Retourne un dict intent standardisé.
        """
        text = text.strip()
        m = re.match(r'^(?:ouvre|ouvrir|lance|lancer)\s+(.+)$', text, re.IGNORECASE)
        if m:
            app_name = m.group(1).strip()
            return {
                "name": "open_app",
                "confidence": 0.9,
                "slots": {"app_name": app_name},
                "raw_text": text
            }
        # fallback générique
        return {
            "name": "unknown",
            "confidence": 0.0,
            "slots": {},
            "raw_text": text
        }

    def parse_intent(self, text: str):
        """
        Tente d'abord IntentEngine.parse() si présent, sinon le parseur local.
        Assure une forme standardisée de l'intent.
        """
        if self.intent_engine is not None and hasattr(self.intent_engine, "parse"):
            try:
                parsed = self.intent_engine.parse(text)
                # Normaliser la forme attendue : name, confidence, slots, raw_text
                if isinstance(parsed, dict) and "name" in parsed:
                    parsed.setdefault("confidence", parsed.get("confidence", 1.0))
                    parsed.setdefault("slots", parsed.get("slots", {}))
                    parsed.setdefault("raw_text", text)
                    return parsed
            except Exception:
                # si IntentEngine casse, on retombe sur le parseur local
                pass
        return self.parse_intent_local(text)

    def handle_text(self, text: str) -> str:
        intent = self.parse_intent(text)
        # Si intent inconnu -> message d'erreur
        if intent.get("name") == "unknown":
            reply = "Désolé, je n'ai pas compris. Peux-tu reformuler ?"
        else:
            # ToolRouter.execute doit retourner soit dict contenant "reply", soit une string
            try:
                result = self.tool_router.execute(intent, text)
                if isinstance(result, dict):
                    reply = result.get("reply", str(result))
                else:
                    reply = str(result)
            except Exception as e:
                reply = f"Erreur interne en traitant la requête : {e}"

        if self.tts:
            try:
                self.tts.speak(reply)
            except Exception:
                pass
        return reply
