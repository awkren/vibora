import logging, time
from PyPDF2 import PdfReader, PdfWriter

# loseless pdf compression

# Taking 0.33  to run (without debugging). 
# If fitz is used, its taking 0.75 (its slower even without adding debugging to the function)
def compress_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  writer = PdfWriter()
  for page in reader.pages:
    page.compress_content_streams() # this is cpu intensive!!!
    writer.add_page(page)
  with open("file.pdf", 'wb') as f:
    writer.write(f)

# This is the same as the function above, but supports debugging
# def compress_pdf(pdf_path):
#   # log loaded file
#   logging.info("Started compressing PDF file: %s", pdf_path)
#   start_time = time.time()
#   reader = PdfReader(pdf_path)
#   writer = PdfWriter()
#   for i, page in enumerate(reader.pages):
#     # log each file that is being compressed
#     logging.debug("Compressing page %d", i+1)
#     page.compress_content_streams()
#     writer.add_page(page)
#   output_file = "file.pdf"
#   with open(output_file, 'wb') as f:
#     writer.write(f)
#   end_time = time.time()
#   elapsed_time = end_time - start_time
#   logging.info("Finished compressing file. Elapsed time %.3f", elapsed_time)