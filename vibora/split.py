import os
from PyPDF2 import PdfReader, PdfWriter

# split pdf pages
def split_pdf(pdf_path):
  fname = os.path.splitext(os.path.basename(pdf_path))[0]
  pdf = PdfReader(pdf_path)
  if len(pdf.pages) == 1:
    print("File has 1 page, can't split it.")
    exit()
  else:
    for page in range(len(pdf.pages)):
      pdf_writer = PdfWriter()
      pdf_writer.add_page(pdf.pages[page])
      output_filename = '{}_page_{}.pdf'.format(
        fname, page + 1)
      with open(output_filename, 'wb') as out:
        pdf_writer.write(out)