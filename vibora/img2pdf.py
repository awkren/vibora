from PIL import Image
import img2pdf

# convert image to pdf
def image_to_pdf(img_path):
  image = Image.open(img_path)
  pdf_bytes = img2pdf.convert(image.filename)
  file = open('file.pdf', 'wb')
  file.write(pdf_bytes)
  image.close()
  file.close()