import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("delta_desk")
logger.setLevel(logging.ERROR)

# Create file handler
file_handler = logging.FileHandler("logs/app_errors.log")
file_handler.setLevel(logging.ERROR)

# Create formatter and attach
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Attach the handler to the logger
logger.addHandler(file_handler)

def log_error(message: str):
    """Convenience function to log an error message."""
    logger.error(message)