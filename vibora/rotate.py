from PyPDF2 import PdfWriter, PdfReader

# rotate pdf file
def rotate_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.rotate(90)
    writer.add_page(page)
  with open('file.pdf', 'wb') as pdf_out:
    writer.write(pdf_out)