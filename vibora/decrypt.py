from PyPDF2 import PdfReader, PdfWriter

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