import logging
import os
from src.infrastructure.config import get_settings

settings = get_settings()
# Ensure logs directory exists
LOG_DIR = os.path.dirname(settings.LOG_FILE_PATH)
LOG_FILE_NAME = os.path.basename(settings.LOG_FILE_PATH)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOG_FILE = os.path.join(LOG_DIR, LOG_FILE_NAME)
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s:%(funcName)s - %(message)s"

# Create and configure logger
logging.basicConfig(
    #level=logging.INFO,
    level=settings.LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Function to get a logger for modules
def get_logger(module_name: str) -> logging.Logger:
    """Returns a configured logger for the given module."""
    return logging.getLogger(module_name)
