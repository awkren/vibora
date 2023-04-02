# if you are on windows, download Poppler and add it to PATH
# go to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version

from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter
import os
import time
import sys
import fitz
import io
from PIL import Image
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError, PDFPopplerTimeoutError
from fpdf import FPDF
import codecs

# convert pdf to png
def pdf_to_png(pdf_path):
  # example: images = convert_from_path(r'C:/path/to/file.pdf')
  images = convert_from_path(pdf_path)
  for i in range(len(images)):
    images[i].save('page' + str(i) + '.png')

# convert pdf to text file
def pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    original_stdout = sys.stdout
    with open('file.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        for page in reader.pages:
            print(page.extract_text())
        sys.stdout = original_stdout

# convert text file to pdf
def txt_to_pdf(txt_path):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", size=12)
  with codecs.open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
      encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
      # using cell() make text overflow depending on the text from the .txt file,
      # as it follows the formatting of the .txt file, ignoring line breaking, etc..
      #  use multi_cell() instead
      pdf.multi_cell(0,10,txt=encoded_line, align='J')
  pdf.output('myfile.pdf')

# extract imgs from pdf
def extract_img_from_pdf(pdf_path):
  file = pdf_path
  pdf_file = fitz.open(file)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
  
    for image_index, img in enumerate(page.get_images(), start=1):
      xref = img[0]
      base_image = pdf_file.extract_image(xref)
      image_bytes = base_image["image"]
      image_ext = base_image["ext"]
      image_name = f"img{image_index}.{image_ext}"
      with open(image_name, "wb") as f:
        f.write(image_bytes)
  
# pypdf2 loseless compression
def compress_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.compress_content_streams() # this is cpu intensive!!!
    writer.add_page(page)
  with open("file.pdf", 'wb') as f:
    writer.write(f)

if __name__ == '__main__':
  # case we type only vibora
  if len(sys.argv) == 1:
    print("Missign arguments, see 'vibora help' for reference on how to use it!")
  # case we type vibora help
  elif sys.argv[1].lower() == 'help':
    print('\nWelcome to vibora :) A PDF tool that lets you convert a PDF to PNG, PDF to text, plus some more awesome things. See below!')
    print("\nPDF TO PNG:\n   To convert a .PDF to .PNG, use: 'vibora pdf2png [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nPDF TO TEXT:\n   To convert a .PDF to .TXT, use: 'vibora pdf2text [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nEXTRACT IMAGES FROM PDF:\n   To extract images from a .PDF file, use: 'vibora extractimg [file].pdf'")
    print('   You will be prompted with the amount of images found, and if you want to proceed or not.')
    print("\nCOMPRESS PDF:\n   To compress a .PDF file, use: 'vibora compress [file].pdf'")
    print('   It will try to compress your file without losing quality or removing content.')
    exit()
  # case we actually pass a valid argument
  else:
    # a command is the arg after the filename. e.g. vibora pdf2png(command) [filename]
    command = sys.argv[1].lower()
    
    # convert pdf to png
    # e.g. vibora pdf2png file.pdf
    if command == 'pdf2png':
      pdf_path = sys.argv[2]
      # check if file exists
      file_exists = os.path.isfile(pdf_path)
      if not file_exists:
        print('File not found. Is the path correct?')
        exit()
      print("Converting your file. Just a second...")
      pdf_to_png(pdf_path)
      time.sleep(2)
      print('File converted!')
      exit()
    
    # convert pdf to text
    # e.g. vibora pdf2text file.pdf
    if command == 'pdf2txt':
      pdf_path = sys.argv[2]
      # check if file exists
      file_exists = os.path.isfile(pdf_path)
      if not file_exists:
        print('File not found. Is the path correct?')
        exit()
      print('Converting you file. Just a second...')
      pdf_to_text(pdf_path)
      time.sleep(2)
      print('File converted!')
      exit()

    # extract imgs from pdf
    # e.g. vibora extractimg file.pdf
    if command == 'extractimg':
      pdf_path = sys.argv[2]
      # check if file exists
      file_exists = os.path.isfile(pdf_path)
      if not file_exists:
        print('File not found. Is the path correct?')
        exit()
      extract_img_from_pdf(pdf_path)
      time.sleep(2)
      print("Just a second...")
      print("All done! Images extracted")
      exit()

    # compress pdf
    # e.g. vibora compress file.pdf
    if command == 'compress':
      pdf_path = sys.argv[2]
      # check if file exists
      file_exists = os.path.isfile(pdf_path)
      if not file_exists:
        print('File not found. Is the path correct?')
        exit()
      compress_pdf(pdf_path)
      print('Compressing your file, just a second...')
      time.sleep(2)
      print('All done! File compressed')

    # convert txt to pdf
    if command == 'txt2pdf':
      txt_path = sys.argv[2]
      # check if the file exists
      file_exists = os.path.isfile(txt_path)
      if not file_exists:
        print("File not found. Is the path correct?")
        exit()
      txt_to_pdf(txt_path)      

    # case command doesn't exist
    else:
      print("Command not recognized. Use 'vibora help' to see all the available commands")