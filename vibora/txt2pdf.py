from fpdf import FPDF
import codecs

# convert text file to pdf
def txt_to_pdf(txt_path):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", size=12)
  with codecs.open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
      encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
      # using cell() make text overflow depending on the text from the .txt file,
      # as it follows the formatting of the .txt file, ignoring line breaking, etc..
      #  use multi_cell() instead
      pdf.multi_cell(0,10,txt=encoded_line, align='J')
  pdf.output('myfile.pdf')