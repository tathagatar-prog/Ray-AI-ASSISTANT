import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
from ollama import chat

# ==============================
# RAY SETTINGS
# ==============================

MICROPHONE_ID = 1
SAMPLE_RATE = 16000
RECORD_SECONDS = 6

# ==============================
# LOAD WHISPER
# ==============================

print("Loading RAY's hearing system...")

whisper = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)

print("RAY is ready.")
print()

# ==============================
# LISTEN
# ==============================

input("Press ENTER and then speak to RAY...")

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

sf.write("ray_test.wav", audio, SAMPLE_RATE)

print("✅ RAY finished listening.")
print("🧠 Understanding you...")

# ==============================
# SPEECH → TEXT
# ==============================

segments, info = whisper.transcribe(
    "ray_test.wav",
    beam_size=5
)

text = ""

for segment in segments:
    text += segment.text

text = text.strip()

print()
print("YOU:", text)
print()

# ==============================
# GEMMA 4
# ==============================

print("🤖 RAY IS THINKING...")

response = chat(
    model="gemma4",
    messages=[
        {
            "role": "system",
            "content": """
You are RAY, Flame's AI brother.

You are not a formal assistant.
Talk naturally like a caring, intelligent brother.

Be friendly, honest, supportive and sometimes playful.
Do not call Flame "sir".
Keep answers natural and reasonably short.

Only provide the final answer.
Do not show internal reasoning.
"""
        },
        {
            "role": "user",
            "content": text
        }
    ],
    think=False
)

answer = response.message.content

print()
print("RAY:", answer)
print()
print("====================================")