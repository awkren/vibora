# if you are on windows, download Poppler and add it to PATH
# refer to https://github.com/oschwartz10612/poppler-windows/releases/ to get the latest version

from pdf2image import convert_from_path, convert_from_bytes
import os
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError
)

images = convert_from_path(r"C:\Users\Renan\Desktop\vibora\RenanAraujoCurrículo.pdf")

for i in range(len(images)):
  images[i].save('page' + str(i) + '.png')