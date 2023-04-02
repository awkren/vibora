import os
import sys
import unittest
from vibora import pdf_to_text, pdf_to_png, extract_img_from_pdf, compress_pdf, txt_to_pdf
import glob # used to delete all images when pdf has multiple pages (pdf2png function)
import codecs

class ViboraTesting(unittest.TestCase):

  # testing pdf to png
  def test_pdf_to_png(self):
    try:
      # call the pdf_to_png function with tompaper.pdf file
      pdf_to_png('testpaper1.pdf')
    except Exception as e:
      self.fail(f"pdf_to_png raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('page0.png'))
    # delete test files
    for file in glob.glob('page*.png'):
      os.remove(file)

  # testing pdf to text
  def test_pdf_to_text(self):
    try:
      # call the pdf_to_text function with tompaper.pdf file
      pdf_to_text('testpaper1.pdf')
    except Exception as e:
      self.fail(f"pdf_to_text raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('file.txt'))
    # check if the output file has content
    with open('file.txt', 'r', encoding='utf-8') as f:
      content = f.read()
      self.assertGreater(len(content), 0)
    # Delete the test files
    os.remove('file.txt')
  
  # testing txt file to pdf
  def test_txt_to_pdf(self):
    try:
      # call the txt_to_pdf function with testpaper3.txt file
      txt_to_pdf('testpaper3.txt')
    except Exception as e:
      self.fail(f"txt_to_pdf raised an unexpected exception: {e}")
    # check if file exists
    self.assertTrue(os.path.exists('myfile.pdf'))
    # delete test files
    os.remove('myfile.pdf')

  # testing extract img from pdf
  def test_img_from_pdf(self):
    try:
      # call the extract_img_from_pdf function with dummy.pdf file
      extract_img_from_pdf('testpaper2.pdf')
    except Exception as e:
      self.fail(f"extract_img_from_pdf raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('img1.png'))
    # delete test files
    for file in glob.glob('img*.png'):
      os.remove(file)

  # testing compress pdf
  def test_compress_pdf(self):
    try:
      #call the compress_pdf function with tompaper.pdf file
      compress_pdf('testpaper1.pdf')
    except Exception as e:
      self.fail(f"compress_pdf raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('file.pdf'))
    # delete test files
    os.remove('file.pdf')

if __name__ == '__main__':
  unittest.main()
