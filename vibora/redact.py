import re, fitz, logging, os, psutil, time

# SOME GOOD THINGS THAT COULD BE ADDED:
# - add a counter of things that can be redacted. i.e `5 emails found, etc`

# redact sensitive information on pdf
# by now, it only removes email, but im working on making it able to detect IDs (documents in general).
# or even taking those as args (e.g. redact only emails or only passwords, etc)
class Redactor:
  @staticmethod
  # function to get all the lines
  def get_sensitive_data(lines):
    # email regex
    EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d\.]+)"

    # cpf regex
    CPF_REG = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"
    
    for line in lines:
      # match regex to each line
      if re.search(EMAIL_REG, line, re.IGNORECASE):
        search = re.search(EMAIL_REG, line, re.IGNORECASE) 
        # yields creates a generator used to return values in between function iterations
        yield search.group(1)
      elif re.search(CPF_REG, line):
        search = re.search(CPF_REG, line)
        yield search.group(0)
  
  # constructor
  def __init__(self, path):
    self.path = path

  # main redactor code
  def redaction(self):

    #log loaded file
    logging.info(f"Started redacting file: {self.path}")
    logging.info(f"File size before redaction: {os.path.getsize(self.path)} bytes")
    start_time = time.monotonic()
    process = psutil.Process(os.getpid())

    # opening pdf file
    doc = fitz.open(self.path)

    # redaction items counter
    redaction_counter = 0

    # iterating through pages
    for page in doc:
      # _wrapContents is used to fix alignment issues with rect boxes
      page.wrap_contents()
      # getting rect boxes which consists the matching email regex
      sensitive = self.get_sensitive_data(page.get_text("text").split('\n'))
      for data in sensitive:
        areas = page.search_for(data)
        # drawing outline over sensitive datas
        [page.add_redact_annot(area, fill = (0,0,0)) for area in areas]

        redaction_counter += 1

        logging.info(f"Redacting item {data}")
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")

      # applying redaction
      page.apply_redactions()

    # saving it to a new pdf
    # outfile = doc.save("redacted.pdf")
    doc.save("redacted.pdf")
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    logging.info(f"File size after redaction: {os.path.getsize('redacted.pdf')} bytes")
    logging.info("Finished redacting file. Elapsed time %.3f", elapsed_time)
    logging.info(f"Total sensitive items redacted: {redaction_counter}")
    # notice that redaction DOES increase the file size
  
