"""
Command Router
--------------
Responsable de dispatcher les commandes vers les bons handlers.
"""

from typing import Callable, Dict


class CommandRouter:
    def __init__(self, app):
        self.app = app
        self._routes: Dict[str, Callable[[str], str]] = {}
        self._register_builtin_routes()

    # =========================
    # Public API
    # =========================

    def register(self, command: str, handler: Callable[[str], str]) -> None:
        """
        Register a new command handler.
        """
        self._routes[command] = handler

    def handle(self, command: str) -> str:
        """
        Handle an incoming command.
        """
        if not command.strip():
            return ""

        command = command.strip()
        keyword = command.split()[0].lower()

        handler = self._routes.get(keyword)

        if handler:
            return handler(command)

        return "❌ Command not recognized."

    # =========================
    # Built-in Commands
    # =========================

    def _register_builtin_routes(self):
        self.register("enregistre", self._handle_remember)
        self.register("donne", self._handle_recall)
        self.register("ai", self._handle_help)

    def _handle_remember(self, command: str) -> str:
        """
        remember <key> <value>
        """
        parts = command.split(" ", 2)

        if len(parts) < 3:
            return "Usage: remember <key> <value>"

        _, key, value = parts
        self.app.memory.set(key, value)

        return f"✅ Stored '{key}'."

    def _handle_recall(self, command: str) -> str:
        """
        recall <key>
        """
        parts = command.split(" ", 1)

        if len(parts) < 2:
            return "Usage: recall <key>"

        _, key = parts
        value = self.app.memory.get(key)

        if value is None:
            return f"⚠️ No value stored for '{key}'."

        return f"📦 {key} = {value}"

    def _handle_help(self, command: str) -> str:
        commands = ", ".join(self._routes.keys())
        return f"Available commands: {commands}"
