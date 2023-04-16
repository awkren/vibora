from PyPDF2 import PdfReader, PdfWriter

# pypdf2 loseless compression
def compress_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.compress_content_streams() # this is cpu intensive!!!
    writer.add_page(page)
  with open("file.pdf", 'wb') as f:
    writer.write(f)