import fitz

# extract imgs from pdf
def extract_img_from_pdf(pdf_path):
  file = pdf_path
  pdf_file = fitz.open(file)
  for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    for image_index, img in enumerate(page.get_images(), start=1):
      xref = img[0]
      base_image = pdf_file.extract_image(xref)
      image_bytes = base_image["image"]
      image_ext = base_image["ext"]
      image_name = f"img{image_index}.{image_ext}"
      with open(image_name, "wb") as f:
        f.write(image_bytes)