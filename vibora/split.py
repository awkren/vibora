import os, time, logging, psutil
from PyPDF2 import PdfReader, PdfWriter

# split pdf pages
def split_pdf(pdf_path, progress_interval=1):
  try:
    logging.info(f"Started spliting PDF file: {pdf_path}")
    logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    fname = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf = PdfReader(pdf_path)
    num = len(pdf.pages)
    progress_counter = 0
    if len(pdf.pages) == 1:
      print("File has 1 page, can't split it.")
      exit()
    else:
      for i, page in enumerate(range(len(pdf.pages))):
        logging.debug(f"Splitting page {i+1}")
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])
        output_filename = '{}_page_{}.pdf'.format(
          fname, page + 1)
        with open(output_filename, 'wb') as out:
          pdf_writer.write(out)
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        if i+1 >= progress_counter + progress_interval or i+1 == num:
          progress_counter = i+1
          progress_percent = progress_counter / num * 100
          logging.info(f"Split {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Finished splitting files. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)