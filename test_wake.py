import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import tempfile
from pathlib import Path
import time

MICROPHONE_ID = 1
SAMPLE_RATE = 16000
RECORD_SECONDS = 2

print("================================")
print("       RAY WAKE WORD TEST")
print("================================")
print()
print('Say "Ray" when you see LISTENING.')
print("Press Ctrl+C to stop.")
print()

print("Loading small local speech model...")

model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("✅ Wake-word system ready.")
print()

while True:

    print("🎤 Listening for: RAY")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MICROPHONE_ID
    )

    sd.wait()

    path = Path(tempfile.gettempdir()) / "ray_wake_test.wav"

    sf.write(
        path,
        audio,
        SAMPLE_RATE
    )

    segments, info = model.transcribe(
        str(path),
        beam_size=1
    )

    text = ""

    for segment in segments:
        text += segment.text

    text = text.strip().lower()

    if text:
        print("HEARD:", text)

    if "ray" in text:

        print()
        print("🔥🔥🔥 RAY WAKE WORD DETECTED! 🔥🔥🔥")
        print()

        time.sleep(1)