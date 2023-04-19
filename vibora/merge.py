import os, time, logging, psutil
from PyPDF2 import PdfMerger

# python main.py merge
# merge pdf files
def merge_pdf(*pdf_files, progress_interval=1):
  try:
    logging.info(f"Started merging files: {pdf_files}")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    total_size = 0
    num = len(pdf_files)
    progress_counter = 0
    for pdf_file in pdf_files:
      file_size = os.path.getsize(pdf_file)
      total_size += file_size
      logging.info(f"Size of {pdf_file}: {file_size} bytes")
    logging.info(f"Total size of files: {total_size} bytes")
    merger = PdfMerger()
    for i, pdf_file in enumerate(pdf_files):
      logging.debug(f"Merging file {i+1}")
      with open(pdf_file, 'rb') as f:
        merger.append(f)
      mem_usage = process.memory_info().rss / 1024 / 1024
      logging.debug(f"Memory usage: {mem_usage:.2f} MB")
      if i+1 >= progress_counter + progress_interval or i+1 == num:
        progress_counter = i+1
        progress_percent = progress_counter / num * 100
        logging.info(f"Merged {progress_counter} of {num} files ({progress_percent:.1f}%)")
    merger.write("merged_file.pdf")
    merger.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after merge: {os.path.getsize('merged_file.pdf')} bytes")
    logging.info("Finished merging files. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)

# python main.py mergeall
# merge pdf files inside folder, ignores non .pdf files
def merge_pdf_directory(directory_path):
  merger = PdfMerger()
  pdf_files = [file for file in os.listdir(directory_path) if file.endswith('.pdf')]
  for pdf_file in pdf_files:
    with open(os.path.join(directory_path, pdf_file), 'rb') as f:
      merger.append(f)
  merger.write(os.path.join(directory_path, 'merged_file.pdf'))
  merger.close()