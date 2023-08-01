import logging, time, os, psutil
from PyPDF2 import PdfReader, PdfWriter

# watermark pdf | to test it use testfiles/file.pdf for the watermark
# watermark is added to bottom left of file.
def watermark_pdf(pdf_path, watermark, progress_interval=1):
    try:
        logging.info(f"Adding watermark to file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        logging.info(f"Watermark file size: {os.path.getsize(watermark)} bytes")
        start_time = time.time()
        process = psutil.Process(os.getpid())
        watermark_instance = PdfReader(watermark)
        watermark_page = watermark_instance.pages[0]
        pdf_reader = PdfReader(pdf_path)
        pdf_writer = PdfWriter()
        num = len(pdf_reader.pages)
        progress_counter = 0
        for i, page in enumerate(range(len(pdf_reader.pages))):
            logging.debug(f"Adding watermark to page {i+1}")
            page = pdf_reader.pages[page]
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)
            mem_usage = process.memory_info().rss / 1024 / 1024
            logging.debug(f"Memory usage: {mem_usage:.2f} MB")
            if i + 1 >= progress_counter + progress_interval or i + 1 == num:
                progress_counter = i + 1
                progress_percent = progress_counter / num * 100
                logging.info(
                    f"Added watermark to {progress_counter} of {num} pages ({progress_percent:.1f}%)"
                )
        with open("watermarked.pdf", "wb") as out:
            pdf_writer.write(out)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(
            f"File size after adding watermark: {os.path.getsize('watermarked.pdf')} bytes"
        )
        logging.info(
            "Finished adding watermark to file. Elapsed time %.3f", elapsed_time
        )
    except Exception as e:
        logging.exception(e)

