import fitz
import io
from PIL import Image

def extract_img_from_pdf(pdf_path):
  pdf_file = fitz.open(pdf_path)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.get_images()
    if image_list:
      print(f"Found a total of {len(image_list)} in page {page_index}")
    else:
        print(f"No images found")
    for image_index, img in enumerate(image_list, start=1):
      xref = img[0]
      base_image = pdf_file.extract_image(xref)
      image_bytes = base_image["image"]
      image_ext = base_image["ext"]
      image = Image.open(io.BytesIO(image_bytes))
      image.save(open(f"Image{page_index+1}_{image_index}.{image_ext}", "wb"))
