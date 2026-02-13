def run_cli(assistant) -> None:
    """
    Simple interactive CLI loop.
    """

    print("Jarvis ready. Type 'exit' to quit.")

    while True:
        user_input = input("> ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            response = assistant.handle_text(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
