from PyPDF2 import PdfReader
import sys, time, os, logging, psutil

# convert pdf to text file
def pdf_to_text(pdf_path, progress_interval=1):
  try:
    logging.info(f"Started converting file: {pdf_path}")
    logging.info(f"Size of file {pdf_path}: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    reader = PdfReader(pdf_path)
    original_stdout = sys.stdout
    num = len(reader.pages)
    progress_counter = 0
    with open('file.txt', 'w', encoding='utf-8') as f:
      sys.stdout = f
      for i, page in enumerate(reader.pages):
        logging.debug(f"Converting page {i+1}")
        print(page.extract_text())
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        if i+1 >= progress_counter + progress_interval or i+1 == num:
          progress_counter = i+1
          progress_percent = progress_counter / num * 100
          logging.info(f"Converted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
      sys.stdout = original_stdout
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Size of {'file.txt'}: {os.path.getsize('file.txt')} bytes")
    logging.info("Finished converting file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)
