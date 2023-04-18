import logging, time, os, psutil
import fitz

# extract imgs from pdf
def extract_img_from_pdf(pdf_path):
  try:
    logging.info(f"Extracting images from file: {pdf_path}")
    logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    file = pdf_path
    pdf_file = fitz.open(file)
    for i, page_index in enumerate(range(len(pdf_file))):
      logging.debug(f"Extracting image from page {i+1}")
      page = pdf_file[page_index]
      for image_index, img in enumerate(page.get_images(), start=1):
        logging.debug(f"Extracting image: {image_index} | Image info: {img}")
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_name = f"img{image_index}.{image_ext}"
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        with open(image_name, "wb") as f:
          f.write(image_bytes)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Done extracting images. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)