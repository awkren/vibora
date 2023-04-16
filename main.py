# if you are on windows, download Poppler and add it to PATH
# go to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version
import time
import sys

from vibora.pdf2png import pdf_to_png
from vibora.pdf2txt import pdf_to_text
from vibora.txt2pdf import txt_to_pdf
from vibora.extract_img_from_pdf import extract_img_from_pdf
from vibora.compress import compress_pdf  
from vibora.merge import merge_pdf, merge_pdf_directory
from vibora.rename import rename_file
from vibora.rotate import rotate_pdf
from vibora.img2pdf import image_to_pdf
from vibora.split import split_pdf
from vibora.watermark import watermark_pdf
from vibora.encrypt import encrypt_pdf
from vibora.decrypt import decrypt_pdf
from vibora.pdf2audio import audio
from vibora.redact import Redactor

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
    print("\nREAD PDF FOR ME:\n   To make vibora read (yes, audio related) a .PDF file, you can use: 'vibora -speak [file].pdf'")
    print("   It will start reading the text of a pdf file for you. You can stop it by pressing CTRL + C.")
    print("\nREDACT SENSITIVE INFORMATIO:\n   To redact sensitive information in a .PDF file, you can use: 'vibora -redact [file].pdf'")
    print("   It will hide sensitive information behind a black rectangle.")
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

      # speak the pdf content      
      case '-speak':
        pdf_path = sys.argv[2]
        # check if file exists
        pdf_exists = os.path.isfile(pdf_path)
        if not pdf_exists:
          print("File not found. Is the path correct?")
        print("Reading file...\nPress CTRL + C after the text is read to stop the -speak command.")
        audio(pdf_path)

      # redact sensitive information
      case '-redact':
        path = sys.argv[2]
        redactor = Redactor(path)
        redactor.redaction()

      # case command doesn't exist
      case _:
        print("Command not recognized. Use 'vibora help' to see all the available commands")