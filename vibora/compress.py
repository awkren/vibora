import logging, time, os, psutil, contextlib
from PyPDF2 import PdfReader, PdfWriter

# Todo:
# Add input validation: Add code to validate that the input file is a PDF file and exists on disk before attempting to compress it. 

# Improve progress reporting: Currently, progress is reported by logging the percentage of pages that have been compressed. 

# Consider adding a progress bar to make it easier to visualize the progress of the compression.

# Add error handling for PyPDF2 exceptions: The compress_content_streams method can raise various exceptions if the PDF file is corrupt or contains unsupported features. 

# Add appropriate error handling to catch these exceptions and log an error message.

# Make the output file name configurable: Allow the user to specify the output file name as a parameter instead of hard-coding it in the function.

# Add support for multiprocessing: The current implementation compresses each page sequentially. 

# Consider using the multiprocessing module to compress pages in parallel and speed up the compression process on multi-core CPUs.

# Refactor the code for readability: Consider refactoring the code to improve readability and make it more modular. 

# For example, move the code that calculates the file size and percentage variation into a separate function.

# Use f-strings consistently: The function currently uses a mix of f-strings and string concatenation. 

# Use f-strings consistently for improved readability and performance.

# Use time.monotonic() for elapsed time: Instead of using time.time() to measure elapsed time, use time.monotonic() to avoid issues with system time changes.

# Add unit tests: Write unit tests to verify that the function works as expected under various conditions.

# loseless pdf compression
def compress_pdf(pdf_path, progress_interval=1):
  # input validation
  if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith('.pdf'):
    raise ValueError("Invalid input file. Please provide a valid PDF file path.")
  try:
    # log loaded file
    logging.info("Started compressing PDF file: %s", pdf_path)
    logging.info(f"File size before compression: {os.path.getsize(pdf_path)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid()) # get current process
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    num = len(reader.pages)
    progress_counter = 0
    
    for i, page in enumerate(reader.pages):
      # log each file that is being compressed
      logging.debug("Compressing page %d", i+1)
      page.compress_content_streams() # cpu intensive
      writer.add_page(page)
      mem_usage = process.memory_info().rss / 1024 / 1024 # in mb
      logging.debug(f"Memory usage: {mem_usage:.2f} MB")
      if i+1 >= progress_counter + progress_interval or i+1 == num:
        progress_counter = i+1
        progress_percent = progress_counter / num * 100
        logging.info(f"Encrypted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    
    # by using a context manager to handle file i/o, instead of a with statement,
    # it ensures the file is properly closed, even if an exception is raised 
    output_file = "file.pdf"
    with open(output_file, 'wb') as f:
      try:
        writer.write(f)
      except Exception as e:
        logging.exception(e)
        raise e

    # it is also possible to use contextlib module to create a context
    # manager for handling file i/o

    # @contextlib.contextmanager
    # def open_output_file(filename):
    #   with open(filename, 'wb') as f:
    #     try:
    #       yield f
    #     except Exception as e:
    #       logging.exception(e)
    #       raise e
   
    # then we can use this context manager in the function like this:
    
    # output_file = 'file.pdf'
    # with open_output_file(output_file) as f:
    #   writer.write(f)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after compression: {os.path.getsize(output_file)} bytes")
    size_variation = os.path.getsize(pdf_path) - os.path.getsize(output_file)
    calc_percentage_variation = size_variation / os.path.getsize(pdf_path)
    calc_percentage_variation = calc_percentage_variation * 100
    logging.info(f"File size variation: -{size_variation} bytes")
    logging.info("Percentage variation compairing to original file: -%.2f%%", calc_percentage_variation)
    logging.info("Finished compressing file. Elapsed time %.3f", elapsed_time)
  
  except Exception as e:
    logging.exception(e)