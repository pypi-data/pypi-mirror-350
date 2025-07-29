import logging
import sys

# file handler
file_handler = logging.FileHandler("radiens.log", delay=True, mode="a")
file_handler.setLevel(logging.DEBUG)

# stream handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)  # log warnings and above to console

# formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(module)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.WARNING)
