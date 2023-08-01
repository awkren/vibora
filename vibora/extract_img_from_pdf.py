import fitz, io, os, time, logging, psutil
from PIL import Image


def extract_img_from_pdf(pdf_path):
    try:
        logging.info(f"Extracting images from file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")

        start_time = time.monotonic()
        process = psutil.Process(os.getpid())

        pdf_file = fitz.open(pdf_path)
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.get_images()
            logging.debug(f"Extracting image from page {page_index + 1}")
            if image_list:
                print(f"Found a total of {len(image_list)} in page {page_index}")
            else:
                print(f"No images found")
            for image_index, img in enumerate(image_list, start=1):
                logging.debug(f"Extracting image {image_index} | Image Info: {img}")
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                mem_usage = process.memory_info().rss / 1024 / 1024
                logging.debug(f"Memory usage: {mem_usage:.2f} MB")

                image = Image.open(io.BytesIO(image_bytes))
                image.save(open(f"Image{page_index+1}_{image_index}.{image_ext}", "wb"))

        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        logging.info(
            "Done extracting image(s) from file. Elapsed time %.3f", elapsed_time
        )

    except Exception as e:
        logging.exception(e)

