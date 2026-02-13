from jarvis.cli import CLI
from jarvis.memory.memory_manager import MemoryManager


class JarvisApp:
    def __init__(self):
        self.memory = MemoryManager()
        self.cli = CLI(self)

    def run(self):
        self.cli.start()


def create_app() -> JarvisApp:
    return JarvisApp()