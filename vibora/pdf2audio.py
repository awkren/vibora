import pyttsx3
import time
from PyPDF2 import PdfReader
import platform

if platform.system() == "Windows":
    from msvcrt import getch
else:
    from getch import getch


# pdf to audio
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def audio(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text = page.extract_text()
            speak_text(text)
            sleep_duration = 0.5
            start_time = time.time()

            while time.time() - start_time < sleep_duration:
                if getch() == b"\x03":  # Check for Ctrl+C key press
                    return  # Exit the function if Ctrl+C is pressed
                else:
                    continue  # to go to the next page automatically
