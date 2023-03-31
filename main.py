# if you are on windows, download Poppler and add it to PATH
# go to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version

from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter
import os
import time
import sys
import fitz
import io
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
from PIL import Image
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError
)

# convert pdf to png function
def pdf_to_png(pdf_path):
  # example: images = convert_from_path(r'C:/path/to/file.pdf')
  images = convert_from_path(pdf_path)
  for i in range(len(images)):
    # this is the name of converted file. change that later, too weird a file always called page[number]
    images[i].save('page' + str(i) + '.png')

# convert pdf to text
def pdf_to_text(pdf_path):
  reader = PdfReader(pdf_path)
  page = reader.pages[0]
  original_stdout = sys.stdout
  with open('file.txt', 'w') as f:
    sys.stdout = f
    print(page.extract_text())
    sys.stdout = original_stdout

# extract imgs from pdf
def extract_img_from_pdf(pdf_path):
  file = pdf_path
  pdf_file = fitz.open(file)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.get_images()
    if image_list:
      one_image = 'image'
      if len(image_list) == 1:
        print(f"Found {len(image_list)} {one_image} in the {file} file.")
      else:
        print(f"Found a total of {len(image_list)} images in the {file} file.")
    else:
      print("No images found on ", page_index)
    choice = input("Do you want to extract the images I found? [YES/NO]\n").lower()
    if choice == 'yes':
      for image_index, img in enumerate(page.get_images(), start=1):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_name = f"page_{page_index}_image_{image_index}.{image_ext}"
        with open(image_name, "wb") as f:
          f.write(image_bytes)
        print(f"Saved {image_name}")
    else:
      exit()
  
# pypdf2 loseless compression
def compress_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.compress_content_streams() # attention! this is cpu intensive!!!
    writer.add_page(page)
  with open("file.pdf", 'wb') as f:
    writer.write(f)

if __name__ == '__main__':
  # case we type python main.py
  if len(sys.argv) == 1:
    print("Missign arguments, see 'python main.py help' for reference on how to use it!")
  # case we type python main.py help
  elif sys.argv[1].lower() == 'help':
    print('\nWelcome to vibora :) A PDF tool that lets you convert a PDF to PNG, PDF to text, plus some more awesome things. See below!')
    print("\nPDF TO PNG:\n   To convert a .PDF to .PNG, use: 'python main.py pdf2png [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nPDF TO TEXT:\n   To convert a .PDF to .TXT, use: 'python main.py pdf2text [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nEXTRACT IMAGES FROM PDF:\n   To extract images from a .PDF file, use: 'python main.py extractimg [file].pdf'")
    print('   You will be prompted with the amount of images found, and if you want to proceed or not.')
    exit()
  # case we actually pass a valid argument
  else:
    # a command is the arg after the filename. e.g. python main.py pdf2png(command) [filename]
    command = sys.argv[1].lower()
    
    # convert pdf to png
    # e.g. python main.py pdf2png | note that it expects a file! -> python main.py pdf2png file.pdf
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
    
    # convert pdf to text
    # e.g. python main.py pdf2text | note that it expects a file! -> python main.py pdf2text file.pdf
    if command == 'pdf2text':
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

    # extract imgs from pdf
    if command == 'extractimg':
      pdf_path = sys.argv[2]
      # check if file exists
      file_exists = os.path.isfile(pdf_path)
      if not file_exists:
        print('File not found. Is the path correct?')
        exit()
      extract_img_from_pdf(pdf_path)
      time.sleep(2)
      print('We are extracting images from the file you provided')
      print("Just a second...")
      print("All done! Images extracted")

    if command == 'compress':
      pdf_path = sys.argv[2]
      compress_pdf(pdf_path )

    else:
      print("Command not recognized. Use 'python main.py help' to see all the available commands")