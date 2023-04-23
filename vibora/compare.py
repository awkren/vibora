import fitz, logging, time, os, psutil

def compare_file(file1, file2):
  try:
    logging.info(f"Starting to compare {file1} and {file2}")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    # open files
    doc1 = fitz.open(file1)
    doc2 = fitz.open(file2)

    # compare n of pages
    logging.info("Comparing number of pages...\n")
    if len(doc1) != len(doc2):
      logging.debug("Length of files do not match!")
      print("Length of files do not match!")
      return False
    else:
      logging.debug("Matching length of files!")
      print("Length of files are the same!")
    
    # compare metadata
    logging.debug("Comparing metadata of files...\n")
    metadata1 = doc1.metadata
    metadata2 = doc2.metadata
    if metadata1 != metadata2:
      logging.debug("Metadata of files do not match!")
      print("Metadata do not match!")
      return False
    else:
      logging.debug("Metadata is the same!")
      print("Metadata is the same!")
    
    # compare content of each page
    logging.debug("Comparing content of each page...\n")
    for i in range(len(doc1)):
      page1 = doc1[i]
      page2 = doc2[i]

      if page1.get_text() != page2.get_text():
        logging.debug(f"Content of page {i+1} do not match!")
      else:
        logging.debug(f"Content of page {i+1} matches!")
      mem_usage = process.memory_info().rss / 1024 / 1024 # in mb
      logging.debug(f"Memory usage: {mem_usage:.2f} MB")
      
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Finished comparing files. Elapsed time %.3f", elapsed_time)
      # also compare the size, the color space, etc.
      # For example:
      # if page1.rect != page2.rect:
      #     return False
  except Exception as e:
    logging.exception(e)
  print(f"Everything matches, files are the same!")
  return True