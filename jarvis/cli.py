class CLI:
    def __init__(self, app):
        self.app = app

    def start(self):
        print("A votre service monsieur")

        while True:
            command = input(">>> ")

            if command.lower() == "exit":
                print("Au revoir.")
                break

            #print(f"You said: {command}")
