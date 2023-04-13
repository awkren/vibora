# if you are on windows, download Poppler and add it to PATH
# go to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version

from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
from os import listdir
import time
import sys
import fitz
import io
from PIL import Image
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError, PDFPopplerTimeoutError
from fpdf import FPDF
import codecs
import pyttsx3
import keyboard
import img2pdf
import threading

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
    
# rename files
def rename_file(file, new_name):
  os.rename(file, new_name)

# rotate pdf file
def rotate_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.rotate(90)
    writer.add_page(page)
  with open('file.pdf', 'wb') as pdf_out:
    writer.write(pdf_out)

# convert image to pdf
def image_to_pdf(img_path):
  image = Image.open(img_path)
  pdf_bytes = img2pdf.convert(image.filename)
  file = open('file.pdf', 'wb')
  file.write(pdf_bytes)
  image.close()
  file.close()

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

# decrypt a pdf file
# IT DOESNT CRACK A PDF FILE!, IT WILL DECRYPT A PDF YOU HAVE THE PASSWORD WITH YOU
def decrypt_pdf(pdf_path, password):
  out = PdfWriter()
  file = PdfReader(pdf_path)
  if file.is_encrypted:
    try:
      # ADD INCORRECT PASSWORD PROMPT LATER
      file.decrypt(password)
      for idx in range(len(file.pages)):
        page = file.pages[idx]
        out.add_page(page)
      with open("file_decrypted.pdf", "wb") as f:
        out.write(f)
    except Exception:
      print(f"An error occured. Is the password correct?")
  else:
    print("File is not encrypted")

# pdf to audio
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def audio(pdf_path):
    with open(pdf_path, 'rb') as f:
      pdf_reader = PdfReader(f)
      # from_page = pdf_reader.pages[3]
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

if __name__ == '__main__':
  # case we type only vibora
  if len(sys.argv) == 1:
    print("Missign arguments, see 'vibora help' for reference on how to use it!")
  # case we type vibora help
  elif sys.argv[1].lower() == 'help':
    print('\nWelcome to vibora :) A PDF tool that lets you convert a PDF to PNG, PDF to text, plus some more awesome things. See below!')
    print("\nPDF TO PNG:\n   To convert a .PDF to .PNG, use: 'vibora -pdf2png [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nPDF TO TEXT:\n   To convert a .PDF to .TXT, use: 'vibora -pdf2text [file].pdf'")
    print('   Remember to provide the full path to the file, and do not forget to add the .pdf at the end ;)')
    print("\nEXTRACT IMAGES FROM PDF:\n   To extract images from a .PDF file, use: 'vibora -extractimg [file].pdf'")
    print('   You will be prompted with the amount of images found, and if you want to proceed or not.')
    print("\nCOMPRESS PDF:\n   To compress a .PDF file, use: 'vibora -compress [file].pdf'")
    print('   It will try to compress your file without losing quality or removing content.')
    print("\nTXT TO PDF:\n   To convert a .TXT file to .PDF, use: 'vibora -txt2pdf [file].txt'")
    print('   It will convert a .txt file into .pdf.')
    print("\nMERGE PDFs:\n   To merge .PDF files into one .PDF, use: 'vibora -merge [file1].pdf [file2].pdf [file3].pdf'")
    print('   It will merge the files provided, without losing quality or cutting content. It can take as many files as you want.')
    print("\nMERGE ALL PDF FILES INSIDE DIRECTORY:\n   To merge all .PDF files inside a directory, use: 'vibora -mf [directory]'")
    print('   It will ignore non .PDF files and merge all .PDF files inside that folder. Files are merged by alphabetical order.')
    print("\nRENAME FILES:\n   To rename files using vibora, you can use: 'vibora -rename [file].pdf [newname].pdf'")
    print('   It will change the name of the file you provided, with the name you typed after it, without affecting th file.')
    print("\nROTATE PDF:\n   To rotate a .PDF file, you can you can use: 'vibora -rotate [file].pdf'")
    print('   It will rotate you file by 90º. Depending on your file, you may want to rotate it multiple times.')
    print("\nIMAGE TO PDF:\n   To convert an image to a .PDF file, you can you can use: 'vibora -img2pdf [file].[extension]'")
    print('   It can convert multiple image formats into a .PDF file.')
    print("\nSPLIT PDF:\n   To split a .PDF file into separated pages, you can you can use: 'vibora -split [file].pdf'")
    print('   It will split the .PDF file into separated pages. Each page from the .PDF will be a single .PDF file.')
    print("\nWATERMARK PDF:\n   To add watermark to a a .PDF file, you can you can use: 'vibora -watermark [file].pdf [watermarkfile].pdf'")
    print('   It will add a watermark to the bottom left of the .PDF file. Remember that the watermark must also be a .PDF file.')
    print("\nENCRYPT PDF:\n   To encrypt a .PDF file, you can you can use: 'vibora -encrypt [file].pdf [password]'")
    print('   It will encrypt a .pdf file by adding a password to be able to read its content.')
    print("\nDECRYPT PDF:\n   To decrypt a .PDF file, you can you can use: 'vibora -decrypt [file].pdf [password]'")
    print("   It will remove the password of a pdf file. Note that it doesn't crack the .pdf file, it works only if you have the password.")
    print("\nREAD PDF FOR ME:\n   To make vibora read (yes, audio related) a .PDF file, you can you can use: 'vibora -speak [file].pdf'")
    print("   It will start reading the text of a pdf file for you. You can stop it by pressing CTRL + C.")
    # exit()
  # case we actually pass a valid argument
  else:
    # a command is the arg after the filename. e.g. vibora pdf2png(command) [filename]
    command = sys.argv[1].lower()
    
    # same as switch in another languages
    match command:

      # convert pdf to png
      # e.g. vibora pdf2png file.pdf
      case "-pdf2png":
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
      case '-pdf2txt':
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
      case '-extractimg':
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
      case '-compress':
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
      case '-txt2pdf':
        txt_path = sys.argv[2]
        # check if the file exists
        file_exists = os.path.isfile(txt_path)
        if not file_exists:
          print("File not found. Is the path correct?")
          exit()
        txt_to_pdf(txt_path)      

      # merge pdfs into one pdf
      case '-merge':
        pdf_files = sys.argv[2:]
        # check if file exists
        print("Merging your files... Just a second.")
        time.sleep(3)
        merge_pdf(*pdf_files)

      # merge folder of pdfs
      case '-mf':
        directory = sys.argv[2]
        merge_pdf_directory(directory)

      # rename files
      case '-rename':
        file = sys.argv[2]
        new_name = sys.argv[3]
        # check if file exists
        file_exists = os.path.isfile(file)
        if not file_exists:
          print("File not found. Is the path correct?")
          exit()
        rename_file(file, new_name)

      # rotate pdf
      case '-rotate':
        pdf_path = sys.argv[2]
        # check if file exists
        file_exists = os.path.isfile(pdf_path)
        if not file_exists:
          print("File not found. Is the path correct?")
          exit()
        print("Rotating your file... Just a second.")
        time.sleep(3)
        rotate_pdf(pdf_path)
        print("File rotated!")
    
      # image to pdf
      case '-img2pdf':
        img_path = sys.argv[2]
        # check if file exists
        file_exists = os.path.isfile(img_path)
        if not file_exists:
          print("File not found. Is the path correct?")
          exit()
        print("Converting your file... Just a second.")
        time.sleep(3)
        image_to_pdf(img_path)
        print("File converted")
  
      # split pdf
      case '-split':
        pdf_path = sys.argv[2]
        # check if file exists
        file_exists = os.path.isfile(pdf_path)
        if not file_exists:
          print("File not found. Is the path correct?")
          exit()
        split_pdf(pdf_path)
        print("Spliting your pdf files... Just a second.")
        time.sleep(3)
        print("PDF split into separated pages")

      # add watermark to pdf
      case '-watermark':
        pdf_path = sys.argv[2]
        watermark = sys.argv[3]
        # check if files exists
        pdf_exists = os.path.isfile(pdf_path)
        watermark_exists = os.path.isfile(watermark)
        if not pdf_exists:
          print("PDF file not found. Is the path correct?")
        if not watermark_exists:
          print("Watermark file not found. Is the path correct?")
        watermark_pdf(pdf_path, watermark)
    
      # encrypt a pdf file
      case '-encrypt':
        pdf_path = sys.argv[2]
        password = sys.argv[3]
        # check if file exists
        pdf_exists = os.path.isfile(pdf_path)
        if not pdf_exists:
          print("File not found. Is the path correct?")
          exit()
        encrypt_pdf(pdf_path, password)

      # decrypt a pdf file
      case '-decrypt':
        pdf_path = sys.argv[2]
        password = sys.argv[3]
        # check if file exists
        pdf_exists = os.path.isfile(pdf_path)
        if not pdf_exists:
          print("File not found. Is the paht correct?")
        decrypt_pdf(pdf_path, password)
      
      case '-speak':
        pdf_path = sys.argv[2]
        # check if file exists
        pdf_exists = os.path.isfile(pdf_path)
        if not pdf_exists:
          print("File not found. Is the path correct?")
        print("Reading file...\nPress CTRL + C after the text is read to stop the -speak command.")
        audio(pdf_path)

      # case command doesn't exist
      case _:
        print("Command not recognized. Use 'vibora help' to see all the available commands")