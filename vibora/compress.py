import logging, time, os, psutil, contextlib, PyPDF2
from multiprocessing import Pool
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

# Todo:
# Make the output file name configurable: Allow the user to specify the output file name as a parameter instead of hard-coding it in the function.
# Add support for multiprocessing: The current implementation compresses each page sequentially. 

# loseless pdf compression
def compress_pdf(pdf_path, progress_interval=1, num_processes=1):
  
  # returns a logger object with the specified name that we can use to customize the logging behavior.
  # this allow us to specify the logging level, add filters, and direct the log messages to specific handlers, among other things.
  logger = logging.getLogger(__name__)

  try:
    # input validation
    if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith('.pdf'):
      raise ValueError("Invalid input file. Please provide a valid PDF file path.")
    
    # number of processes validation
    if not isinstance(num_processes, int) or num_processes < 1:
      raise ValueError("Number of processes must be a positive integer")

    # log loaded file
    logging.info(f"Started compressing PDF file: {pdf_path}")
    logging.info(f"File size before compression: {os.path.getsize(pdf_path)} bytes")
    start_time = time.monotonic() # time.monotonic was used to avoid issues with system time changes
    process = psutil.Process(os.getpid()) # get current process 
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    num = len(reader.pages)
    progress_counter = 0

    # define compress_page function to use with multiprocessing
    def compress_page(page):
      page.compress_content_streams()
      return page

      # use multiprocessing to compress pages in parallel
    if num_processes > 1:
      with Pool(processes=num_processes) as pool:
          compressed_pages = pool.map(compress_page, reader.pages)
    else:
      compressed_pages = [compress_page(page) for page in reader.pages]
    
    with tqdm(total=num, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]") as pbar:
      # here we pass compressed pages to the writer instead of the usual "raw" reader
      for i, page in enumerate(compressed_pages):
        writer.add_page(page)
        mem_usage = process.memory_info().rss / 1024 / 1024
        logging.debug(f"Memory usage: {mem_usage:.2f} MB")
        if i+1 >= progress_counter + progress_interval or i+1 == num:
          progress_counter = i+1
          progress_percent = progress_counter / num * 100
          logging.info(f"Compressed {progress_counter} of {num} pages ({progress_percent:.1f}%)")
          pbar.update(1)

    # WITHOUT MULTIPROCESSING
    # for i, page in enumerate(reader.pages):
    #   # log each file that is being compressed
    #   logging.debug(f"Compressing page {i+1}")
    #   page.compress_content_streams() # cpu intensive
    #   writer.add_page(page)
    #   mem_usage = process.memory_info().rss / 1024 / 1024 # in mb
    #   logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    #   if i+1 >= progress_counter + progress_interval or i+1 == num:
    #     progress_counter = i+1
    #     progress_percent = progress_counter / num * 100
    #     logging.info(f"Encrypted {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    
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

    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    logging.info(f"File size after compression: {os.path.getsize(output_file)} bytes")
    size_variation = os.path.getsize(pdf_path) - os.path.getsize(output_file)
    calc_percentage_variation = size_variation / os.path.getsize(pdf_path)
    calc_percentage_variation = calc_percentage_variation * 100
    logging.info(f"File size variation: -{size_variation} bytes")
    logging.info("Percentage variation compairing to original file: -%.2f%%", calc_percentage_variation)
    logging.info("Finished compressing file. Elapsed time %.3f", elapsed_time)
  
  except PyPDF2.utils.PdfReadError as e:
    # catch the PdfReadError exception raised by PyPDF2
    logger.error(f"Error reading PDF file: {e}")

  except PyPDF2.utils.PdfStreamErorr as e:
    # catch the PdfStreamError exception raised by PyPDF2
    logger.error(f"Error in PDF stream: {e}")

  except Exception as e:
    # catch any other exceptions raised during the execution of the code
    logger.error(f"Unexpected error occurred: {e}")