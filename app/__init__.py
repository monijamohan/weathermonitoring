import logging

# # Config Default # To log in the Running container
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()],
)

# # Configure the logger | File Handler
file_handler = logging.FileHandler('fast_api.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logging.getLogger().addHandler(file_handler)
