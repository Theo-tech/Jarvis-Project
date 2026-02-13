from jarvis.core.assistant import Assistant

def test_greeting():
    a = Assistant()
    assert "bonjour" in a.handle("Bonjour").lower() or "comment" in a.handle("Bonjour").lower()