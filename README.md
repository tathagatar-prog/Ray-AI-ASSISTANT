# RAY V1 — Flame's AI Brother

RAY is a Windows desktop AI companion being built step by step.

## V1 features

- RAY desktop dashboard
- RAY robot image
- Internet status
- Microphone recording
- Speech-to-text
- OpenAI conversation
- Text-to-speech

## Setup

1. Install Python 3.11 or newer.
2. Open this folder in VS Code.
3. Create a virtual environment:

   python -m venv .venv

4. Activate it in PowerShell:

   .\.venv\Scripts\Activate.ps1

5. Install packages:

   pip install -r requirements.txt

6. Copy `.env.example` to `.env`.
7. Put your OpenAI API key in `.env`.
8. Run:

   python main.py

## Important

Never put your API key into GitHub or share it publicly.

V1 deliberately uses a push-to-talk button. Always-listening / wake-word mode
will be added after the basic system works reliably.
