import sounddevice as sd
import numpy as np
import tempfile
import wave
import time
from faster_whisper import WhisperModel

class SpeechToText:
    def __init__(self):
        self.sample_rate = 16000
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    def listen(self):
        print("🎤 Parle...")

        silence_threshold = 500  # ajuste si besoin
        silence_duration = 1.0   # secondes de silence avant stop
        chunk_duration = 0.1     # 100 ms

        chunk_size = int(self.sample_rate * chunk_duration)
        silence_time = 0
        recording = []
        started = False

        stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=chunk_size,
        )

        with stream:
            while True:
                data, _ = stream.read(chunk_size)
                volume = np.linalg.norm(data)

                if volume > silence_threshold:
                    if not started:
                        print("🗣️ Détection voix...")
                        started = True
                    recording.append(data)
                    silence_time = 0
                else:
                    if started:
                        silence_time += chunk_duration
                        recording.append(data)

                    if started and silence_time > silence_duration:
                        break

        print("🧠 Transcription...")

        audio_data = np.concatenate(recording)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wf = wave.open(f.name, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
            wf.close()

            segments, _ = self.model.transcribe(
                f.name,
                language="fr",
                beam_size=5,
                vad_filter=True
            )

        text = " ".join([seg.text for seg in segments])
        return text.strip()
