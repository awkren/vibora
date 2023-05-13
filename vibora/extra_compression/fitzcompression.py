import fitz, io
from PIL import Image

def fitzcomp(pdf_path):
  doc = fitz.open(pdf_path)

  for page_num in range(doc.page_count):
    page = doc[page_num]
    img_list = page.get_images(full=True)

    for img_info in img_list:
      xref = img_info[0]
      base_image = fitz.Pixmap(doc, xref)
      img_data = base_image.samples

      # compress img using PIL
      img = Image.open(io.BytesIO(img_data))
      img_compressed = io.BytesIO()
      img.save(img_compressed, format='JPEG', quality=50)

      # replace the img in the pdf
      doc.update_image(xref, img_compressed.getvalue())
    
  doc.save('fitzFile.pdf', garbage=4, deflate=True)