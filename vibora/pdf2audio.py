import keyboard, pyttsx3, threading
from PyPDF2 import PdfReader

# pdf to audio
def speak_text(text):
  engine = pyttsx3.init()
  engine.say(text)
  engine.runAndWait()

def audio(pdf_path):
  with open(pdf_path, 'rb') as f:
    pdf_reader = PdfReader(f)
    for page in pdf_reader.pages:
      text = page.extract_text()
    # using threading to run the engine in a separated thread, allowing us to stop the engine
    # otherwise, pyttsx3 would run til it finishes reading...
      t = threading.Thread(target=speak_text, args=(text,))
      t.daemon = True
      t.start()
    # t.join()
    # while True:
    #   if keyboard.is_pressed('ctrl+c'):
    #     sys.exit(0)
  while True:
    if keyboard.is_pressed('ctrl+c'):
      break