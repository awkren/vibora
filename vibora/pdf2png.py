from pdf2image import convert_from_path

# convert pdf to png
def pdf_to_png(pdf_path):
  # example: images = convert_from_path(r'C:/path/to/file.pdf')
  images = convert_from_path(pdf_path)
  for i in range(len(images)):
    images[i].save('page' + str(i) + '.png')