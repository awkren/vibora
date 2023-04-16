import os
from PyPDF2 import PdfMerger

# merge pdf files
def merge_pdf(*pdf_files):
  merger = PdfMerger()
  for pdf_file in pdf_files:
    with open(pdf_file, 'rb') as f:
      merger.append(f)
  merger.write("merged_pdf.pdf")
  merger.close()

# merge pdf files inside folder, ignores non .pdf files
def merge_pdf_directory(directory_path):
  merger = PdfMerger()
  pdf_files = [file for file in os.listdir(directory_path) if file.endswith('.pdf')]
  for pdf_file in pdf_files:
    with open(os.path.join(directory_path, pdf_file), 'rb') as f:
      merger.append(f)
  merger.write(os.path.join(directory_path, 'merged_file.pdf'))
  merger.close()