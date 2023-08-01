import logging, time, os, psutil
from PyPDF2 import PdfWriter, PdfReader

# rotate pdf file
def rotate_pdf(pdf_path, progress_interval=1):
    try:
        logging.info(f"Rotating file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time = time.time()
        process = psutil.Process(os.getpid())
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        num = len(reader.pages)
        progress_counter = 0
        for i, page in enumerate(reader.pages):
            logging.debug(f"Rotating page {i+1}")
            page.rotate(90)
            writer.add_page(page)
            mem_usage = process.memory_info().rss / 1024 / 1024
            logging.debug(f"Memory usage: {mem_usage:.2f} MB")
            if i + 1 >= progress_counter + progress_interval or i + 1 == num:
                progress_counter = i + 1
                progress_percent = progress_counter / num * 100
                logging.info(
                    f"Rotated {progress_counter} of {num} pages ({progress_percent:.1f}%)"
                )
        with open("file.pdf", "wb") as pdf_out:
            writer.write(pdf_out)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"File size after rotation: {os.path.getsize(pdf_path)} bytes")
        logging.info("Finished rotating file. Elapsed time %.3f", elapsed_time)
    except Exception as e:
        logging.exception(e)

