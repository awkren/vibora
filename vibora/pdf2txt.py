from PyPDF2 import PdfReader
import sys

# convert pdf to text file
def pdf_to_text(pdf_path):
  reader = PdfReader(pdf_path)
  original_stdout = sys.stdout
  with open('file.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    for page in reader.pages:
      print(page.extract_text())
    sys.stdout = original_stdout