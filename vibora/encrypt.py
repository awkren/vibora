import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# encrypt a pdf file
def encrypt_pdf(pdf_path, password, progress_interval=1, num_threads=1):
  try:
    logging.info(f"Started encrypting PDF file: {pdf_path}")
    logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid()) # get current process
    out = PdfWriter()
    file = PdfReader(pdf_path)
    num = len(file.pages)
    progress_counter = 0
    with tqdm(total=num, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]") as pbar, ThreadPoolExecutor(max_workers=num_threads) as executor:
      futures = []
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
          pbar.update(1)
        if i % num_threads == 0 or i == num - 1:
          # submit a batch of pages to be encrypted in parallel
          futures.append(executor.submit(_encrypt_pages, out, password, process))
          out = PdfWriter()
      for future in futures:
        future.result() # wait for all batches to finish
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after encryption: {os.path.getsize(pdf_path)} bytes")
    logging.info("Finished encrypting file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)

def _encrypt_pages(out, password, process):
  out.encrypt(password) # AES-128 encryption by default
  with open("file.pdf", 'ab') as f:
    out.write(f)