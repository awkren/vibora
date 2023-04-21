import re, fitz

# redact sensitive information on pdf
# by now, it only removes email, but im working on making it able to detect IDs (documents in general).
# or even taking those as args (e.g. redact only emails or only passwords, etc)
class Redactor:
  @staticmethod
  # function to get all the lines
  def get_sensitive_data(lines):
    
    #email regex
    EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+)"
    for line in lines:
      # match regex to each line
      if re.search(EMAIL_REG, line, re.IGNORECASE):
        search =  re.search(EMAIL_REG, line, re.IGNORECASE)
        # yields creates a generator used to return values in between function iterations
        yield search.group(1)
  
  # constructor
  def __init__(self, path):
    self.path = path

  # main redactor code
  def redaction(self):

    # opening pdf file
    doc = fitz.open(self.path)
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

      # applying redaction
      page.apply_redactions()

    # saving it to a new pdf
    doc.save("redacted.pdf")
