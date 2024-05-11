import logging

def get_logger():
    # # Config Default # To log in the Running container
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[logging.StreamHandler()],
    )

    # # # Configure the logger | File Handler
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # log_file_path = os.path.join(current_dir, 'fast_api.log')

    # Get the absolute path of the logs directory mounted via Docker Compose
    log_file_path = '/code/logs/fast_api.log'
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logging.getLogger().addHandler(file_handler)
    logging.info("---------------Logger Initiated")
    return logging


logger = get_logger()
