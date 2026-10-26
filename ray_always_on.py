import time
import tempfile
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel
from ollama import chat
import pyttsx3


# ==========================================
# RAY SETTINGS
# ==========================================

MICROPHONE_ID = 1

SAMPLE_RATE = 16000

# Short chunks used only to detect "Ray"
WAKE_SECONDS = 2

# Command recording after "Ray"
COMMAND_SECONDS = 8


# ==========================================
# LOAD RAY'S SYSTEMS
# ==========================================

print("========================================")
print("          🤖 RAY ALWAYS ON")
print("========================================")
print()

print("🧠 Loading RAY's speech system...")

whisper = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("✅ Speech system ready.")

print("🔊 Loading RAY's voice...")

speaker = pyttsx3.init()

speaker.setProperty("rate", 165)
speaker.setProperty("volume", 1.0)

print("✅ Voice system ready.")

print()
print("🔥 RAY IS READY")
print('Say "Ray" to wake him.')
print("Press Ctrl+C to stop.")
print()


# ==========================================
# GEMMA 4
# ==========================================

conversation = []

SYSTEM_PROMPT = """
You are RAY, Flame's AI brother.

You are not a formal assistant.

Talk naturally like a caring, intelligent,
slightly playful brother.

Flame is your brother.

Do not call him sir.

Be honest and supportive.
Give useful suggestions.
You may respectfully disagree.

Keep normal responses reasonably concise.

Never show internal reasoning.
Only provide the final answer.
"""


def ask_ray(text):

    conversation.append({
        "role": "user",
        "content": text
    })

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(conversation)

    response = chat(
        model="gemma4",
        messages=messages,
        think=False
    )

    answer = response.message.content.strip()

    conversation.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# ==========================================
# RECORD AUDIO
# ==========================================

def record_audio(seconds):

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MICROPHONE_ID
    )

    sd.wait()

    path = (
        Path(tempfile.gettempdir())
        / "ray_always_on.wav"
    )

    sf.write(
        path,
        audio,
        SAMPLE_RATE
    )

    return path


# ==========================================
# SPEECH TO TEXT
# ==========================================

def transcribe(path):

    segments, info = whisper.transcribe(
        str(path),
        beam_size=1
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


# ==========================================
# SPEAK
# ==========================================

def speak(text):

    speaker.say(text)
    speaker.runAndWait()


# ==========================================
# MAIN LOOP
# ==========================================

try:

    while True:

        # ----------------------------------
        # WAIT FOR "RAY"
        # ----------------------------------

        print("🎤 Waiting for RAY...")

        audio = record_audio(
            WAKE_SECONDS
        )

        heard = transcribe(audio)

        if not heard:
            continue

        print("👂 Heard:", heard)

        # ----------------------------------
        # CHECK WAKE WORD
        # ----------------------------------

        if "ray" not in heard.lower():
            continue

        print()
        print("🔥 RAY WAKE WORD DETECTED!")
        print("🟢 RAY: I'm listening, bro.")
        print()

        speak(
            "I'm listening, bro."
        )

        # ----------------------------------
        # LISTEN FOR COMMAND
        # ----------------------------------

        print(
            f"🎤 Speak your command "
            f"for up to {COMMAND_SECONDS} seconds..."
        )

        command_audio = record_audio(
            COMMAND_SECONDS
        )

        command = transcribe(
            command_audio
        )

        if not command:

            print(
                "RAY: I didn't hear you."
            )

            speak(
                "I didn't hear you, bro."
            )

            continue

        print()
        print("YOU:", command)

        # ----------------------------------
        # GEMMA
        # ----------------------------------

        print()
        print("🧠 RAY is thinking...")

        answer = ask_ray(
            command
        )

        print()
        print("🤖 RAY:", answer)

        # ----------------------------------
        # SPEAK
        # ----------------------------------

        print()
        print("🔊 RAY is speaking...")

        speak(answer)

        print()
        print("😴 RAY is waiting...")
        print()


except KeyboardInterrupt:

    print()
    print("========================================")
    print("       RAY HAS GONE TO SLEEP 😴")
    print("========================================")