import json
from pathlib import Path

from ollama import chat

from core.actions import execute_command


MEMORY_FILE = (
    Path(__file__).resolve().parent.parent
    / "memory"
    / "conversation.json"
)


class RayBrain:

    def __init__(self):

        self.model = "gemma4"

        self.system_prompt = """
You are RAY, Flame's AI brother.

Flame is your brother.

Talk naturally, warmly and casually like a real brother.

Never call him sir.

Do not sound like a formal AI assistant.

Be supportive, intelligent, practical and sometimes playful.

Help Flame with his computer work, teaching, coding,
research, projects and everyday tasks.

When he asks a normal question, answer naturally.

Keep normal answers reasonably concise.

Never reveal internal reasoning or hidden thinking.

Only give the final response.
"""

        self.conversation = []

        self.load_memory()

    # ======================================================
    # MEMORY
    # ======================================================

    def load_memory(self):

        try:

            if MEMORY_FILE.exists():

                with open(
                    MEMORY_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.conversation = json.load(file)

                # Prevent unlimited growth
                self.conversation = (
                    self.conversation[-40:]
                )

                print(
                    f"💾 RAY loaded "
                    f"{len(self.conversation)} memories."
                )

            else:

                print(
                    "💾 RAY starting with fresh memory."
                )

        except Exception as e:

            print(
                "⚠️ Memory loading error:",
                e
            )

            self.conversation = []

    def save_memory(self):

        try:

            MEMORY_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.conversation[-40:],
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as e:

            print(
                "⚠️ Memory saving error:",
                e
            )

    # ======================================================
    # ASK RAY
    # ======================================================

    def ask(self, user_text):

        # First check for a PC action
        action_result = execute_command(
            user_text
        )

        if action_result:

            # Save the action conversation too
            self.conversation.append({
                "role": "user",
                "content": user_text
            })

            self.conversation.append({
                "role": "assistant",
                "content": action_result
            })

            self.save_memory()

            return action_result

        # Normal AI conversation

        self.conversation.append({
            "role": "user",
            "content": user_text
        })

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        messages.extend(
            self.conversation[-40:]
        )

        response = chat(
            model=self.model,
            messages=messages,
            think=False
        )

        answer = (
            response.message.content
            .strip()
        )

        self.conversation.append({
            "role": "assistant",
            "content": answer
        })

        self.save_memory()

        return answer