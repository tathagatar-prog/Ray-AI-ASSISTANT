from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFrame
)

from core.brain import RayBrain
from voice.internet import internet_available
from voice.recorder import record_wav
from voice.transcriber import Transcriber
from voice.speaker import Speaker


ASSET = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "ray.png"
)


# ==========================================================
# WORKER
# ==========================================================

class Worker(QThread):

    status = Signal(str)
    user_text = Signal(str)
    ray_text = Signal(str)
    error = Signal(str)

    def __init__(self, brain):

        super().__init__()

        self.brain = brain

    def run(self):

        try:

            self.status.emit(
                "🎤 RAY is listening..."
            )

            audio = record_wav(8)

            self.status.emit(
                "🧠 RAY is understanding..."
            )

            text = Transcriber().transcribe(
                audio
            )

            if not text:

                self.error.emit(
                    "I didn't hear anything, brother."
                )

                return

            self.user_text.emit(text)

            self.status.emit(
                "🧠 RAY is thinking..."
            )

            answer = self.brain.ask(
                text
            )

            self.ray_text.emit(
                answer
            )

            self.status.emit(
                "🔊 RAY is speaking..."
            )

            # IMPORTANT:
            # Speaker is persistent and can speak
            # multiple times.
            Speaker().speak(
                answer
            )

            self.status.emit(
                "🟢 RAY is Online"
            )

        except Exception as e:

            print(
                "WORKER ERROR:",
                e
            )

            self.error.emit(
                str(e)
            )

            self.status.emit(
                "🟢 RAY is Online"
            )


# ==========================================================
# MAIN WINDOW
# ==========================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "RAY — Flame's AI Brother"
        )

        self.resize(
            1050,
            720
        )

        self.setMinimumSize(
            850,
            600
        )

        # ONE brain for the whole application
        self.brain = RayBrain()

        # ONE speaker for the whole application
        self.speaker = Speaker()

        self.worker = None

        # --------------------------------------------------
        # ROOT
        # --------------------------------------------------

        root = QWidget()

        self.setCentralWidget(
            root
        )

        layout = QVBoxLayout(
            root
        )

        layout.setContentsMargins(
            28,
            24,
            28,
            24
        )

        layout.setSpacing(
            16
        )

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = QLabel(
            "🔥 FLAME  &  RAY 🤖"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Segoe UI",
                26,
                QFont.Bold
            )
        )

        layout.addWidget(
            title
        )

        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        self.status = QLabel()

        self.status.setAlignment(
            Qt.AlignCenter
        )

        self.update_status()

        layout.addWidget(
            self.status
        )

        # --------------------------------------------------
        # MAIN CARD
        # --------------------------------------------------

        card = QFrame()

        card.setObjectName(
            "card"
        )

        card_layout = QHBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        # --------------------------------------------------
        # RAY IMAGE
        # --------------------------------------------------

        self.robot = QLabel()

        self.robot.setAlignment(
            Qt.AlignCenter
        )

        if ASSET.exists():

            pixmap = QPixmap(
                str(ASSET)
            )

            self.robot.setPixmap(
                pixmap.scaled(
                    390,
                    390,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        card_layout.addWidget(
            self.robot,
            1
        )

        # --------------------------------------------------
        # RIGHT PANEL
        # --------------------------------------------------

        right = QVBoxLayout()

        welcome = QLabel(
            "Hey brother.\nI'm RAY. I'm here."
        )

        welcome.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Bold
            )
        )

        right.addWidget(
            welcome
        )

        # --------------------------------------------------
        # CHAT
        # --------------------------------------------------

        self.chat = QTextEdit()

        self.chat.setReadOnly(
            True
        )

        self.chat.setPlaceholderText(
            "Your conversation with RAY will appear here..."
        )

        right.addWidget(
            self.chat,
            1
        )

        # --------------------------------------------------
        # TALK BUTTON
        # --------------------------------------------------

        self.talk = QPushButton(
            "🎙  TALK TO RAY"
        )

        self.talk.setMinimumHeight(
            58
        )

        self.talk.clicked.connect(
            self.start_talk
        )

        right.addWidget(
            self.talk
        )

        card_layout.addLayout(
            right,
            1
        )

        layout.addWidget(
            card,
            1
        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        hint = QLabel(
            "Speak naturally. RAY can open apps, websites "
            "and help you with your work."
        )

        hint.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            hint
        )

        # --------------------------------------------------
        # STYLE
        # --------------------------------------------------

        self.setStyleSheet("""

            QMainWindow, QWidget {
                background: #07111f;
                color: #eaf7ff;
            }

            #card {
                background: #0d1b2a;
                border: 1px solid #173e5a;
                border-radius: 24px;
            }

            QTextEdit {
                background: #081522;
                border: 1px solid #174563;
                border-radius: 14px;
                padding: 12px;
                color: #eaf7ff;
                font-size: 15px;
            }

            QPushButton {
                background: #0b8fd6;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #19a8ef;
            }

            QPushButton:disabled {
                background: #334a5c;
            }

        """)

    # ======================================================
    # STATUS
    # ======================================================

    def update_status(self):

        if internet_available():

            self.status.setText(
                "🟢  RAY is Online"
            )

        else:

            self.status.setText(
                "🔴  RAY is Offline"
            )

    # ======================================================
    # TALK
    # ======================================================

    def start_talk(self):

        if not internet_available():

            self.update_status()

            self.chat.append(
                "RAY: Brother, you're offline right now. "
                "Connect to the internet and try again."
            )

            return

        self.talk.setEnabled(
            False
        )

        self.status.setText(
            "🔵  RAY is listening..."
        )

        self.worker = Worker(
            self.brain
        )

        self.worker.status.connect(
            self.status.setText
        )

        self.worker.user_text.connect(
            lambda text:
            self.chat.append(
                f"<b>Flame:</b> {text}"
            )
        )

        self.worker.ray_text.connect(
            lambda text:
            self.chat.append(
                f"<b>RAY:</b> {text}"
            )
        )

        self.worker.error.connect(
            lambda text:
            self.chat.append(
                f"<b>RAY:</b> ⚠️ {text}"
            )
        )

        self.worker.finished.connect(
            self.talk_finished
        )

        self.worker.start()

    # ======================================================
    # FINISHED
    # ======================================================

    def talk_finished(self):

        self.talk.setEnabled(
            True
        )

        self.update_status()


# ==========================================================
# RUN
# ==========================================================

def run():

    app = QApplication([])

    window = MainWindow()

    window.show()

    app.exec()