from jarvis.core.tool_router import ToolRouter
from jarvis.core.assistant import Assistant
from jarvis.services.launcher import build_open_app_handler
from jarvis.cli import run_cli


def create_app() -> Assistant:
    """
    Create and configure the Jarvis application.
    """

    router = ToolRouter()
    router.register("open_app", build_open_app_handler())

    assistant = Assistant(router=router)

    return assistant


def run() -> None:
    """
    Start the Jarvis application.
    """

    assistant = create_app()
    run_cli(assistant)
