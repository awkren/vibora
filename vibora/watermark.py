from PyPDF2 import PdfReader, PdfWriter

# watermark pdf
def watermark_pdf(pdf_path, watermark):
  watermark_instance = PdfReader(watermark)
  watermark_page = watermark_instance.pages[0]
  pdf_reader = PdfReader(pdf_path)
  pdf_writer = PdfWriter()
  for page in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page]
    page.merge_page(watermark_page)
    pdf_writer.add_page(page)
  with open('watermarked.pdf', 'wb') as out:
    pdf_writer.write(out)