import fitz

def compare_file(file1, file2):
  # open files
  doc1 = fitz.open(file1)
  doc2 = fitz.open(file2)

  # compare n of pages
  if len(doc1) != len(doc2):
    print("Length do not match!")
  
  # compare metadata
  metadata1 = doc1.metadata
  metadata2 = doc2.metadata
  if metadata1 != metadata2:
    print("Metadata do not match!")
  
  # compare content of each page
  for i in range(len(doc1)):
    page1 = doc1[i]
    page2 = doc2[i]

    if page1.get_text() != page2.get_text():
      print(f"Content of page {i} do not match!")
    
    # You can also compare other properties of the pages, such as the size, the color space, etc.
    # For example:
    # if page1.rect != page2.rect:
    #     return False
  print(f"Everything matches, files are the same!")
  return True