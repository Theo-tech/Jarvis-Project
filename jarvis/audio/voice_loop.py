from jarvis.audio.stt import SpeechToText
from jarvis.audio.tts import TextToSpeech
from jarvis.services.llm_client import LLMClient


def run_voice_mode():
    stt = SpeechToText()
    tts = TextToSpeech()
    llm = LLMClient()

    print("🎙 Mode vocal activé. Dis 'stop' pour quitter.\n")

    while True:
        user_text = stt.listen()

        if not user_text:
            continue

        print(f"Vous > {user_text}")

        if "stop" in user_text.lower():
            tts.speak("À bientôt.")
            break

        response = llm.chat(user_text)

        print(f"Jarvis > {response}")
        tts.speak(response)
