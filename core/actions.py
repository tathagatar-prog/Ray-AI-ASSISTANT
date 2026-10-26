import os
import subprocess
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus


# ==========================================================
# HELPER
# ==========================================================

def launch(path):

    try:

        os.startfile(str(path))
        return True

    except Exception as e:

        print("Launch error:", e)
        return False


# ==========================================================
# WEB
# ==========================================================

def open_youtube(search=None):

    if search:

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(search)
        )

    else:

        url = "https://www.youtube.com"

    webbrowser.open(url)

    if search:
        return f"I opened YouTube and searched for {search}, bro."

    return "YouTube is open, bro."


def open_google(search=None):

    if search:

        url = (
            "https://www.google.com/search?q="
            + quote_plus(search)
        )

        webbrowser.open(url)

        return f"I searched Google for {search}, bro."

    webbrowser.open("https://www.google.com")

    return "Google is open, bro."


# ==========================================================
# WINDOWS APPLICATIONS
# ==========================================================

def open_word():

    try:

        subprocess.Popen(
            ["cmd", "/c", "start", "", "winword"]
        )

        return "Microsoft Word is open, bro."

    except Exception as e:

        return f"I couldn't open Word: {e}"


def open_excel():

    try:

        subprocess.Popen(
            ["cmd", "/c", "start", "", "excel"]
        )

        return "Microsoft Excel is open, bro."

    except Exception as e:

        return f"I couldn't open Excel: {e}"


def open_vscode():

    try:

        subprocess.Popen(["code"])

        return "VS Code is open, bro."

    except FileNotFoundError:

        paths = [

            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Programs"
            / "Microsoft VS Code"
            / "Code.exe",

            Path(
                "C:/Program Files/Microsoft VS Code/Code.exe"
            ),

        ]

        for path in paths:

            if path.exists():

                subprocess.Popen([str(path)])

                return "VS Code is open, bro."

        return "I couldn't find VS Code on your PC."


def open_devcpp():

    paths = [

        Path("C:/Program Files/Dev-Cpp/devcpp.exe"),

        Path("C:/Program Files (x86)/Dev-Cpp/devcpp.exe"),

        Path("C:/Dev-Cpp/devcpp.exe"),

        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs"
        / "Dev-Cpp"
        / "devcpp.exe",

    ]

    for path in paths:

        if path.exists():

            subprocess.Popen([str(path)])

            return "Dev-C++ is open, bro."

    return (
        "I couldn't find Dev-C++ automatically. "
        "We'll add its exact location later."
    )


def open_notepad():

    try:

        subprocess.Popen(["notepad.exe"])

        return "Notepad is open, bro."

    except Exception as e:

        return f"I couldn't open Notepad: {e}"


def open_calculator():

    try:

        subprocess.Popen(["calc.exe"])

        return "Calculator is open, bro."

    except Exception as e:

        return f"I couldn't open Calculator: {e}"


# ==========================================================
# WINDOWS FOLDERS
# ==========================================================

def open_folder(folder):

    folder = Path(folder)

    if folder.exists():

        launch(folder)

        return f"I opened {folder.name}, bro."

    return f"I couldn't find the folder {folder}."


def open_documents():

    return open_folder(
        Path.home() / "Documents"
    )


def open_downloads():

    return open_folder(
        Path.home() / "Downloads"
    )


def open_desktop():

    return open_folder(
        Path.home() / "Desktop"
    )


# ==========================================================
# RAY PROJECT
# ==========================================================

def open_ray_project():

    ray_folder = Path("D:/RAY")

    if ray_folder.exists():

        launch(ray_folder)

        return "I opened the RAY project folder, bro."

    return "I couldn't find the RAY project folder."


# ==========================================================
# ACTION DETECTOR
# ==========================================================

def execute_command(text):

    command = text.lower().strip()

    # ------------------------------------------------------
    # YOUTUBE SEARCH
    # ------------------------------------------------------

    if "youtube" in command:

        search = command

        phrases = [
            "open youtube and search for",
            "open youtube and search",
            "search youtube for",
            "search youtube",
            "play on youtube",
            "open youtube",
        ]

        for phrase in phrases:

            search = search.replace(
                phrase,
                ""
            )

        search = search.strip()

        if search:

            return open_youtube(search)

        return open_youtube()

    # ------------------------------------------------------
    # GOOGLE
    # ------------------------------------------------------

    if (
        "search google for" in command
        or "google search" in command
        or "search google" in command
    ):

        search = command

        for phrase in [
            "search google for",
            "search google",
            "google search",
        ]:

            search = search.replace(
                phrase,
                ""
            )

        return open_google(search.strip())

    # ------------------------------------------------------
    # WORD
    # ------------------------------------------------------

    if (
        "open word" in command
        or "open microsoft word" in command
        or "start word" in command
    ):

        return open_word()

    # ------------------------------------------------------
    # EXCEL
    # ------------------------------------------------------

    if (
        "open excel" in command
        or "open microsoft excel" in command
        or "start excel" in command
    ):

        return open_excel()

    # ------------------------------------------------------
    # VS CODE
    # ------------------------------------------------------

    if (
        "open vs code" in command
        or "open vscode" in command
        or "open visual studio code" in command
        or "start vs code" in command
    ):

        return open_vscode()

    # ------------------------------------------------------
    # DEV-C++
    # ------------------------------------------------------

    if (
        "open dev c" in command
        or "open dev-c" in command
        or "open devcpp" in command
        or "open dev c++" in command
    ):

        return open_devcpp()

    # ------------------------------------------------------
    # CALCULATOR
    # ------------------------------------------------------

    if (
        "open calculator" in command
        or "start calculator" in command
    ):

        return open_calculator()

    # ------------------------------------------------------
    # NOTEPAD
    # ------------------------------------------------------

    if (
        "open notepad" in command
        or "start notepad" in command
    ):

        return open_notepad()

    # ------------------------------------------------------
    # DOCUMENTS
    # ------------------------------------------------------

    if (
        "open documents" in command
        or "open my documents" in command
    ):

        return open_documents()

    # ------------------------------------------------------
    # DOWNLOADS
    # ------------------------------------------------------

    if (
        "open downloads" in command
        or "open my downloads" in command
    ):

        return open_downloads()

    # ------------------------------------------------------
    # DESKTOP
    # ------------------------------------------------------

    if (
        "open desktop" in command
        or "show desktop" in command
    ):

        return open_desktop()

    # ------------------------------------------------------
    # RAY PROJECT
    # ------------------------------------------------------

    if (
        "open ray project" in command
        or "open ray folder" in command
        or "open my ray project" in command
    ):

        return open_ray_project()

    return None