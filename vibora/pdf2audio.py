import pyttsx3
import time
from PyPDF2 import PdfReader

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
            time.sleep(0.5)  # Adjust the sleep duration as needed
                             # It is the delay to start reading the next page
            
