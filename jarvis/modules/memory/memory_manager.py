# memory_manager.py

import json
from pathlib import Path

class MemoryManager:
    def __init__(self, path="jarvis/memory/storage.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}")
        self.memory = self._load()

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

    def set(self, key, value):
        self.memory[key] = value
        self.save()

    def get(self, key):
        return self.memory.get(key)
