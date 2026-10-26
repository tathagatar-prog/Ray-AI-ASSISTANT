import pyttsx3
import threading


class Speaker:

    _engine = None
    _lock = threading.Lock()

    def __init__(self):
        self._initialize()

    def _initialize(self):

        if Speaker._engine is not None:
            return

        try:

            engine = pyttsx3.init("sapi5")

            engine.setProperty("rate", 165)
            engine.setProperty("volume", 1.0)

            # Try to select an English voice
            voices = engine.getProperty("voices")

            for voice in voices:

                name = str(getattr(voice, "name", "")).lower()

                if (
                    "david" in name
                    or "mark" in name
                    or "zira" in name
                    or "english" in name
                ):

                    engine.setProperty(
                        "voice",
                        voice.id
                    )

                    break

            Speaker._engine = engine

        except Exception as e:

            print("Speaker initialization error:", e)
            Speaker._engine = None

    def speak(self, text):

        if not text:
            return

        with Speaker._lock:

            try:

                self._initialize()

                if Speaker._engine is None:
                    print("❌ RAY voice engine unavailable.")
                    return

                engine = Speaker._engine

                engine.stop()

                engine.say(str(text))

                engine.runAndWait()

            except Exception as e:

                print("⚠️ RAY speech error:", e)

                # Reinitialize SAPI if it fails
                try:

                    Speaker._engine = None

                    self._initialize()

                except Exception:
                    pass