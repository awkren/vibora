import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter

# loseless pdf compression

# Taking 0.33  to run (without debugging). 
# If fitz is used, its taking 0.75 (its slower even without adding debugging to the function)
# def compress_pdf(pdf_path):
#   reader = PdfReader(pdf_path)
#   writer = PdfWriter()
#   for page in reader.pages:
#     page.compress_content_streams() # this is cpu intensive!!!
#     writer.add_page(page)
#   with open("file.pdf", 'wb') as f:
#     writer.write(f)

# This is the same as the function above, but supports debugging
def compress_pdf(pdf_path):
  # log loaded file
  logging.info("Started compressing PDF file: %s", pdf_path)
  logging.info(f"File size before compression: {os.path.getsize(pdf_path)} bytes")
  start_time = time.time()
  process = psutil.Process(os.getpid()) # get current process
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for i, page in enumerate(reader.pages):
    # log each file that is being compressed
    logging.debug("Compressing page %d", i+1)
    page.compress_content_streams()
    writer.add_page(page)
    mem_usage = process.memory_info().rss / 1024 / 1024 # in mb
    logging.debug(f"Memory usage: {mem_usage:.2f} MB")
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

# TO DO: LOG ERRORS AND EXCEPTIONS THAT MAY HAPPEN