import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
import tempfile
import scipy.io.wavfile as wav


class SpeechToText:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def listen(self, duration=5, sample_rate=16000):
        print("🎤 Parle...")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, sample_rate, recording)
            segments, info = self.model.transcribe(
                f.name,
                language="fr",
                beam_size=5,
                vad_filter=True
            )


        text = " ".join([segment.text for segment in segments])

        return text.strip()
