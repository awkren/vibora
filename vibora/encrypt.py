import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter

# encrypt a pdf file

# taking 0.33 to run this and 0.32 ~ 0.35 with debugging
# def encrypt_pdf(pdf_path, password):
#   out = PdfWriter()
#   file = PdfReader(pdf_path)
#   num = len(file.pages)
#   for idx in range(num):
#     page = file.pages[idx]
#     out.add_page(page)
#   out.encrypt(password)
#   with open("file.pdf", 'wb') as f:
#     out.write(f)  

def encrypt_pdf(pdf_path, password, progress_interval=1):
  try:
    logging.info(f"Started encrypting PDF file: {pdf_path}")
    logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid()) # get current process
    out = PdfWriter()
    file = PdfReader(pdf_path)
    num = len(file.pages)
    progress_counter = 0
    for i, idx in enumerate(range(num)):
      logging.debug(f"Encrypting page {i+1}")
      page = file.pages[idx]
      out.add_page(page)
      mem_usage = process.memory_info().rss / 1024 / 1024
      logging.debug(f"Memory usage: {mem_usage:.2f} MB")
      if i+1 >= progress_counter + progress_interval or i+1 == num:
        progress_counter = i+1
        progress_percent = progress_counter / num * 100
        logging.info(f"Encrypted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    out.encrypt(password)
    with open("file.pdf", 'wb') as f:
      out.write(f)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after encryption: {os.path.getsize(pdf_path)}")
    logging.info("Finished encrypting file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)