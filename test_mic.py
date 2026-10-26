import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

# Your built-in microphone
MICROPHONE_ID = 1

# Recording settings
SAMPLE_RATE = 16000
RECORD_SECONDS = 6

print("====================================")
print("        RAY MICROPHONE TEST")
print("====================================")
print()
print("Get ready...")
print("Speak clearly for 6 seconds.")
print()

input("Press ENTER when you are ready...")

print()
print("🎤 RAY IS LISTENING...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=MICROPHONE_ID
)

sd.wait()

print("✅ Recording finished.")

# Save recording
sf.write("ray_test.wav", audio, SAMPLE_RATE)

print("🎧 Processing your voice...")
print("First time may take a little while because Whisper needs to download its model.")

# Load local Whisper model
model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    "ray_test.wav",
    beam_size=5
)

text = ""

for segment in segments:
    text += segment.text

print()
print("====================================")
print("RAY HEARD:")
print(text.strip())
print("====================================")