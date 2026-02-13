# C:\Projects\main.py
from pathlib import Path
from jarvis.services.launcher import build_open_app_handler
# Si tu implements IndexScanner dans jarvis.services.scanner, importe-le :
# from jarvis.services.scanner import IndexScanner

def main():
    # Si tu as IndexScanner, décommente et initialise proprement :
    # scanner = IndexScanner(roots=["C:\\", "D:\\"], index_path=Path("C:\\Projects\\file_index.json"))
    # scanner.start()

    # Initialisation minimale du router/assistant — ici on suppose que tu as un ToolRouter et Assistant
    try:
        from jarvis.core.tool_router import ToolRouter
        from jarvis.core.assistant import Assistant
    except Exception as e:
        print("Impossible d'importer ToolRouter/Assistant :", e)
        return

    router = ToolRouter()
    # enregistre le handler 'open_app' (ex: intent "open_app")
    router.register("open_app", build_open_app_handler())

    assistant = Assistant(router=router)

    # point d'entrée CLI simple (si tu as cli.py, lance-le)
    try:
        from jarvis.cli import repl
        repl.run(assistant)  # adapte selon ton API
    except Exception:
        # fallback simple : boucle d'entrée utilisateur
        print("Entrée interactive (tape 'exit' pour quitter).")
        while True:
            text = input("> ")
            if not text:
                continue
            if text.strip().lower() in ("exit", "quit"):
                break
            # ici tu dois appeler ton assistant pour traiter la commande
            try:
                result = assistant.handle_text(text)
                print("=>", result)
            except Exception as e:
                print("Erreur assistant:", e)

    # if scanner is running, stop it gracefully
    # try:
    #     scanner.stop()
    # except NameError:
    #     pass

if __name__ == "__main__":
    main()
