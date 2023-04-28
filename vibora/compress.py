import logging, time, os, psutil, contextlib, PyPDF2
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
from typing import Optional

# SOME INTERESTING THINGS TO ADD:

# error handling: 
# add more comprehensive error handling for cases where the input file is not a valid PDF or if there are issues with the output file.

# configurable compression levels: 
# add the ability to configure the compression level to allow for more fine-grained control over the resulting file size and quality.

# caching:
# add a caching mechanism to avoid recompressing files that have already been compressed. 
# this could save a significant amount of time and resources when processing large numbers of files.
# - i think this could be done by creating a cache dir, and adding there info about compressed files and check there.

# logging improvements:
# add more detailed logging to track the progress of the function, including the time taken to compress the file, 
# the compression ratio achieved, and any errors that occur.

# input validation: 
# ensure that the output argument is a valid file name before attempting to write to it.

# support for other file formats: 
# add support for other file formats, such as JPEG and PNG, to allow for lossless compression of images.

# compression format: 
# allow for the selection of different compression formats, such as gzip or bzip2, depending on the requirements of the user.

# output directory: 
# add an option to specify the output directory where the compressed file should be saved.

# user interaction: 
# allow for user interaction to prompt for confirmation before overwriting an existing file with the same name as the output file.

# lossless pdf compression
def compress_pdf(pdf_path, output: Optional[str] = None, progress_interval=1, num_processes=1, num_threads=1):
  
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

    # MULTIPROCESSING VS MULTITHREADING
    # you can use whatever you want here, even the raw function (without any of these options)
    #
    # multiprocessing uses two or more CPUs to increase computing power, whereas multithreading uses a single process with multiple code segments to increase computing power. 
    # multithreading focuses on generating computing threads from a single process, whereas multiprocessing increases computing power by adding CPUs.
    #
    # multiprocessing seems very unstable, as its runtime varies a lot,
    # multithreading keeps a solid runtime of 54 sec compressing a 150mb pdf file.

    # HERE WE USE MULTITHREADING
    def compress_page(page):
      page.compress_content_streams()
      return page
    # use multithreading to compress pages in parallel
    if num_threads > 1:
      with ThreadPoolExecutor(max_workers=num_threads) as executor:
        compressed_pages = list(executor.map(compress_page, reader.pages))
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

    # HERE WE USE MULTIPROCESSING
    # def compress_page(page):
    #   page.compress_content_streams()
    #   return page
    #   # use multiprocessing to compress pages in parallel
    # if num_processes > 1:
    #   with Pool(processes=num_processes) as pool:
    #      compressed_pages = pool.map(compress_page, reader.pages)
    # else:
    #   compressed_pages = [compress_page(page) for page in reader.pages]   
    # with tqdm(total=num, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]") as pbar:
    #   # here we pass compressed pages to the writer instead of the usual "raw" reader
    #   for i, page in enumerate(compressed_pages):
    #     writer.add_page(page)
    #     mem_usage = process.memory_info().rss / 1024 / 1024
    #     logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    #     if i+1 >= progress_counter + progress_interval or i+1 == num:
    #       progress_counter = i+1
    #       progress_percent = progress_counter / num * 100
    #       logging.info(f"Compressed {progress_counter} of {num} pages ({progress_percent:.1f}%)")
    #       pbar.update(1)

    # THIS IS THE RAW CODE ( NO MULTIPROCESSING NOR MULTITHREADING)
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
    
    # ABOUT CONTEXT MANAGER
    # by using a context manager to handle file i/o, instead of a with statement,
    # it ensures the file is properly closed, even if an exception is raised
    if output == None:
      output_file = "file.pdf" # if an output name is not passed, it creates a file.pdf by default
      with open(output_file, 'wb') as f:
        try:
          writer.write(f)
        except Exception as e:
          logging.exception(e)
          raise e
    else:
      output_file = output + '.pdf'# if an output name is passed, it receives its name
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
  
  # except PyPDF2._utils.PdfReadError as e:
  #   # catch the PdfReadError exception raised by PyPDF2
  #   logger.error(f"Error reading PDF file: {e}")

  # except PyPDF2.utils.PdfStreamErorr as e:
  #   # catch the PdfStreamError exception raised by PyPDF2
  #   logger.error(f"Error in PDF stream: {e}")

  except Exception as e:
    # catch any other exceptions raised during the execution of the code
    logger.error(f"Unexpected error occurred: {e}")