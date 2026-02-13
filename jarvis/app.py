from jarvis.cli import CLI
from jarvis.modules.memory.memory_manager import MemoryManager
from jarvis.core.router import CommandRouter


class JarvisApp:
    def __init__(self):
        self.memory = MemoryManager()
        self.router = CommandRouter(self)
        self.cli = CLI(self)

    def run(self):
        self.cli.start()


def create_app() -> JarvisApp:
    return JarvisApp()
