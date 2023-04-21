from fpdf import FPDF
import codecs, os, logging, time, psutil

# convert text file to pdf
def txt_to_pdf(txt_path):
  try:
    logging.info(f"Started converting file: {txt_path}")
    logging.info(f"TXT file size: {os.path.getsize(txt_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with codecs.open(txt_path, 'r', encoding='utf-8') as f:
      logging.debug(f"Converting file {txt_path} to .PDF")
      for line in f:
        encoded_line = line.encode('latin-1', 'replace').decode('latin-1')
        # using cell() make text overflow depending on the text from the .txt file,
        # as it follows the formatting of the .txt file, ignoring line breaking, etc..
        # use multi_cell() instead
        pdf.multi_cell(0,10,txt=encoded_line, align='J')
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    pdf.output('myfile.pdf')
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"PDF file size: {os.path.getsize('myfile.pdf')} bytes")
    logging.info("Finished converting file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)