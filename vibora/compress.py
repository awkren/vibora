import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter

# loseless pdf compression
def compress_pdf(pdf_path, progress_interval=1):
  try:
    # log loaded file
    logging.info("Started compressing PDF file: %s", pdf_path)
    logging.info(f"File size before compression: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid()) # get current process
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    num = len(reader.pages)
    progress_counter = 0
    for i, page in enumerate(reader.pages):
      # log each file that is being compressed
      logging.debug("Compressing page %d", i+1)
      page.compress_content_streams() # cpu intensive
      writer.add_page(page)
      mem_usage = process.memory_info().rss / 1024 / 1024 # in mb
      logging.debug(f"Memory usage: {mem_usage:.2f} MB")
      if i+1 >= progress_counter + progress_interval or i+1 == num:
        progress_counter = i+1
        progress_percent = progress_counter / num * 100
        logging.info(f"Encrypted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    output_file = "file.pdf"
    with open(output_file, 'wb') as f:
      writer.write(f)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after compression: {os.path.getsize(output_file)} bytes")
    size_variation = os.path.getsize(pdf_path) - os.path.getsize(output_file)
    calc_percentage_variation = size_variation / os.path.getsize(pdf_path)
    calc_percentage_variation = calc_percentage_variation * 100
    logging.info(f"File size variation: -{size_variation} bytes")
    logging.info("Percentage variation compairing to original file: -%.2f%%", calc_percentage_variation)
    logging.info("Finished compressing file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)
# TO DO: LOG ERRORS AND EXCEPTIONS THAT MAY HAPPEN