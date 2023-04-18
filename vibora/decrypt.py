import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter

# decrypt a pdf file
# IT DOESNT CRACK A PDF FILE!, IT WILL DECRYPT A PDF YOU HAVE THE PASSWORD WITH YOU
def decrypt_pdf(pdf_path, password, progress_interval=1):
  try:
    out = PdfWriter()
    file = PdfReader(pdf_path)
    if file.is_encrypted:
      try:
        logging.info(f"Started decrypting PDF file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time = time.time()
        process = psutil.Process(os.getpid()) # get current process
        file.decrypt(password)
        num = len(file.pages)
        progress_counter = 0
        for i, idx in enumerate(range(len(file.pages))):
          logging.debug(f"Decrypting page {i+1}")
          page = file.pages[idx]
          out.add_page(page)
          mem_usage = process.memory_info().rss / 1024 / 1024
          logging.debug(f"Memory usage: {mem_usage:.2f} MB")
          if i+1 >= progress_counter + progress_interval or i+1 == num:
            progress_counter = i+1
            progress_percent = progress_counter / num * 100
            logging.info(f"Decrypted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
        with open("file_decrypted.pdf", "wb") as f:
          out.write(f)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Fize size after decryption: {os.path.getsize(pdf_path)} bytes")
        logging.info("Finished decrypting file. Elapsed tiem %.3f", elapsed_time)
      except Exception:
        print(f"An error occured. Is the password correct?")
    else:
      print("File is not encrypted")
  except Exception as err1:
    logging.exception(err1)