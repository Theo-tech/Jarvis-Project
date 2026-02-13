"""
Entry point for Jarvis.
No business logic here.
"""

from jarvis.app import create_app


def run() -> None:
    app = create_app()
    app.run()


if __name__ == "__main__":
    run()
