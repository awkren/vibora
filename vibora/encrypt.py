from PyPDF2 import PdfReader, PdfWriter

# encrypt a pdf file
def encrypt_pdf(pdf_path, password):
  out = PdfWriter()
  file = PdfReader(pdf_path)
  num = len(file.pages)
  for idx in range(num):
    page = file.pages[idx]
    out.add_page(page)
  out.encrypt(password)
  with open("file.pdf", 'wb') as f:
    out.write(f)