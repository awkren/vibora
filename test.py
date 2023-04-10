import os
import sys
import unittest
from vibora import pdf_to_text, pdf_to_png, extract_img_from_pdf, compress_pdf, txt_to_pdf, merge_pdf, rename_file, rotate_pdf, image_to_pdf, split_pdf, watermark_pdf, encrypt_pdf
import glob
import codecs
import shutil

class ViboraTesting(unittest.TestCase):

  # testing pdf to png
  def test_pdf_to_png(self):
    try:
      # call the pdf_to_png function with testpaper1.pdf file
      pdf_to_png('testfiles/testpaper1.pdf')
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
      # call the pdf_to_text function with testpaper1.pdf file
      pdf_to_text('testfiles/testpaper1.pdf')
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
      txt_to_pdf('testfiles/testpaper3.txt')
    except Exception as e:
      self.fail(f"txt_to_pdf raised an unexpected exception: {e}")
    # check if file exists
    self.assertTrue(os.path.exists('myfile.pdf'))
    # delete test files
    os.remove('myfile.pdf')

  # testing extract img from pdf
  def test_img_from_pdf(self):
    try:
      # call the extract_img_from_pdf function with testpaper2.pdf file
      extract_img_from_pdf('testfiles/testpaper2.pdf')
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
      #call the compress_pdf function with testpaper1.pdf file
      compress_pdf('testfiles/testpaper1.pdf')
    except Exception as e:
      self.fail(f"compress_pdf raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('file.pdf'))
    # delete test files
    os.remove('file.pdf')

  # testing merge pdf
  def test_merge_pdf(self):
    try:
      # call the merge_pdf function with testpaper1.pdf and testpaper2.pdf files
      merge_pdf('testfiles/testpaper1.pdf', 'testfiles/testpaper2.pdf')
    except Exception as e:
      self.fail(f"merge_pdf raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('merged_pdf.pdf'))
    # delete test file
    os.remove('merged_pdf.pdf')

  # testing rename files
  def test_rename_file(self):
    try:
      # call the rename_file function with the antigo.pdf file
      rename_file('testfiles/testpaper4.txt', 'new.txt')
    except Exception as e:
      self.fail(f"rename_file raised an unexpected exception: {e}")
    # check fi the outfile file exists and match the name we changed
    self.assertTrue(os.path.exists('new.txt'))
    rename_file('new.txt', 'testpaper4.txt')
    shutil.move('testpaper4.txt', 'testfiles/testpaper4.txt')
  
  # testing rotate files
  def test_rotate_pdf(self):
    try:
      # call the rotate_pdf funtion with the rotate.pdf file
      rotate_pdf('testfiles/rotate.pdf')
    except Exception as e:
      self.fail(f"rotate_pdf raised an unexpected exception: {e}")
    # check if output file matches with result
    self.assertTrue(os.path.exists('file.pdf'))
    # delete test file
    os.remove('file.pdf')

  # testing image to pdf
  def test_image_to_pdf(self):
    try:
      # call the image_to_pdf function with the testfile.png file
      image_to_pdf('testfiles/testfile.png')
    except Exception as e:
      self.fail(f"image_to_pdf raised an unexpected exception: {e}")
    # check if the output file exists
    self.assertTrue(os.path.exists('file.pdf'))
    # delete test file
    os.remove('file.pdf')
  
  # testing split pdf
  def test_split_pdf(self):
    try:
      # call the split_pdf function with the testpaper1.pdf file
      split_pdf('testfiles/testpaper1.pdf')
    except Exception as e:
      self.fail(f"split_pdf raised an unexpected exception: {e}")
    # check the output file
    self.assertTrue(os.path.exists('testpaper1_page_1.pdf'))
    # delete test files
    for file in glob.glob('*.pdf'):
      os.remove(file)
  
  # testing watermark pdf
  def test_watermark_pdf(self):
    try:
      # call the watermark_pdf function with testpaper1.pdf and file.pdf files
      watermark_pdf('testfiles/testpaper1.pdf', 'testfiles/file.pdf')
    except Exception as e:
      self.fail(f"watermark_pdf raised an unexpected exception: {e}")
    # check the output file
    self.assertTrue(os.path.exists('watermarked.pdf'))
    # delete test files
    os.remove('watermarked.pdf')
  
  # testing encrypt pdf
  def test_encrypt_pdf(self):
    try:
      # call the encrypt pdf function with testpaper1.pdf file
      encrypt_pdf("testfiles/testpaper1.pdf")
    except Exception as e:
      self.fail(f"encrypt_pdf raised an unexpectede exception: {e}")
    # check the output file
    self.assertTrue(os.path.exists('file.pdf'))
    # delete test file
    os.remove('file.pdf')

if __name__ == '__main__':
  unittest.main()
