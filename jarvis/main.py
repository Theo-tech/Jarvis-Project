"""
Jarvis - Entry Point
--------------------
Point d'entrée principal de l'application.
Aucune logique métier ici.
"""

from jarvis.app import create_app


def main() -> None:
    """Application entrypoint."""
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
