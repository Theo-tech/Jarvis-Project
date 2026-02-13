# jarvis/core/intent_engine.py
class IntentEngine:
    def parse(self, text: str) -> dict:
        txt = text.lower().strip()
        if any(w in txt for w in ("bonjour", "salut", "coucou")):
            return {"name": "greet", "confidence": 0.9, "slots": {}}
        if any(w in txt for w in ("heure", "quelle heure", "il est")):
            return {"name": "get_time", "confidence": 0.9, "slots": {}}
        if txt.startswith("exécute ") or txt.startswith("run "):
            # simple slot extraction
            cmd = text.split(" ", 1)[1] if " " in text else ""
            return {"name": "run_cmd", "confidence": 0.8, "slots": {"cmd": cmd}}
        return {"name": "unknown", "confidence": 0.0, "slots": {}}
