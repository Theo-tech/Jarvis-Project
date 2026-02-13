"""
CLI Interface
-------------
Manages user interaction loop.
"""

class CLI:
    def __init__(self, app):
        self.app = app

    def start(self):
        print("🤖 Jarvis is running.")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                command = input(">>> ").strip()

                if not command:
                    continue

                if command.lower() in ("exit", "quit"):
                    print("👋 Goodbye.")
                    break

                response = self.app.router.handle(command)

                if response:
                    print(response)

            except KeyboardInterrupt:
                print("\n👋 Interrupted. Goodbye.")
                break

            except Exception as e:
                print(f"⚠️ Error: {e}")
