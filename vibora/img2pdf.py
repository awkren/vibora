import img2pdf, logging, time, os, psutil
from PIL import Image

# convert image to pdf
def image_to_pdf(img_path):
  try:
    logging.info(f"Converting file '{img_path}' to PDF")
    logging.info(f"File size: {os.path.getsize(img_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open('file.pdf', 'wb')
    file.write(pdf_bytes)
    image.close()
    file.close()
    mem_usage = process.memory_info().rss / 1024 / 1024
    logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"PDF file size: {os.path.getsize('file.pdf')} bytes")
    logging.info("Finished converting image to PDF. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)