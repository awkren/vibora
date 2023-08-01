import logging, time, os, psutil, pathlib
from pdf2image import convert_from_path

# convert pdf to png
def pdf_to_png(pdf_path, progress_interval=1):
    try:
        logging.info(f"Converting PDF file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        logging.info(
            f"Files that have more than one page, will be converted into multiple images!"
        )
        start_time = time.time()
        process = psutil.Process(os.getpid())
        images = convert_from_path(pdf_path)
        num = len(images)
        progress_counter = 0
        for i, j in enumerate(range(len(images))):
            logging.debug(f"Converting page {j+1}")
            images[i].save("page" + str(i) + ".png")
            mem_usage = process.memory_info().rss / 1024 / 1024
            logging.debug(f"Memory usage: {mem_usage:.2f} MB")
            if i + 1 >= progress_counter + progress_interval or i + 1 == num:
                progress_counter = i + 1
                progress_percent = progress_counter / num * 100
                logging.info(
                    f"Converted {progress_counter} of {num} pages ({progress_percent:.1f}%)"
                )
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"Image size: {os.path.getsize(pdf_path)} bytes")
            logging.info("Finished converting file. Elapsed time %.3f", elapsed_time)
    except Exception as e:
        logging.exception(e)

