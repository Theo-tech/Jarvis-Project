def test_flow():
    from jarvis.core.assistant import Assistant
    from jarvis.voice.tts import TTS
    a = Assistant(tts=TTS())
    r = a.handle_text("Bonjour")
    assert "Bonjour" in r or "Bonjour" in r.lower()
