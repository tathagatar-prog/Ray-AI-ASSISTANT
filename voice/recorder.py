import tempfile
from pathlib import Path

import sounddevice as sd
import soundfile as sf


SAMPLE_RATE = 16000
CHANNELS = 1

# RAY will use your built-in Realtek microphone
MICROPHONE_ID = 1


def record_wav(seconds: int = 8, device: int = MICROPHONE_ID) -> Path:

    path = Path(tempfile.gettempdir()) / "ray_recording.wav"

    print(f"🎤 Using microphone device: {device}")

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=device,
    )

    sd.wait()

    sf.write(
        path,
        audio,
        SAMPLE_RATE
    )

    return path