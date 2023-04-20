import os, time, logging, psutil

# rename files
def rename_file(file, new_name):
  try:
    logging.info(f"Renaming file {file}")
    logging.info(f"File size: {os.path.getsize(file)} bytes")
    start_time = time.time()
    process = psutil.Process(os.getpid())
    os.rename(file, new_name)
    mem_usage = process.memory_info().rss / 1024 / 1024
    logging.debug(f"Memory usage: {mem_usage:.2f} MB")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"File size after changing name: {os.path.getsize(new_name)} bytes")
    logging.info("Finished renaming file. Elapsed time %.3f", elapsed_time)
  except Exception as e:
    logging.exception(e)