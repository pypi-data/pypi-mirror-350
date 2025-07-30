import logging
from datetime import UTC, datetime

logger = logging.getLogger(f"{__name__}-{datetime.now(UTC)}")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler("example.log")
file_handler.setLevel(logging.ERROR)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define a formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger():
    return logger
