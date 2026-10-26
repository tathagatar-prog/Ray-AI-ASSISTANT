from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self):
        print("Loading RAY's hearing system...")

        self.model = WhisperModel(
            "base.en",
            device="cpu",
            compute_type="int8"
        )

        print("RAY's hearing system is ready.")

    def transcribe(self, audio_path):
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5
        )

        text = ""

        for segment in segments:
            text += segment.text

        return text.strip()