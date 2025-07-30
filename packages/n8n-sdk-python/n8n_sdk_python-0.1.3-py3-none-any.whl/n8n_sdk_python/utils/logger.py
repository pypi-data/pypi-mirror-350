import logging
import logging.handlers
import os
import sys


# Define log format string and date format for standard logging
_LOG_FORMAT_STR = "%(asctime)s,%(msecs)03d | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
_DATE_FORMAT_STR = "%Y-%m-%d %H:%M:%S"

# Ensure the logs directory exists
_LOG_DIR = "logs"
_LOG_FILE_PATH = os.path.join(_LOG_DIR, "n8n_sdk_python.log")

# Create directory if it doesn't exist
if not os.path.exists(_LOG_DIR):
    os.makedirs(_LOG_DIR)

# Get a logger instance
log = logging.getLogger("n8n_sdk_python")
log.setLevel(logging.DEBUG)  # Set the logger's base level; handlers can have their own levels

# Create a formatter
_formatter = logging.Formatter(_LOG_FORMAT_STR, datefmt=_DATE_FORMAT_STR)

# Configure console handler (stdout)
_stdout_handler = logging.StreamHandler(sys.stdout)
_stdout_handler.setLevel(logging.INFO)
_stdout_handler.setFormatter(_formatter)
log.addHandler(_stdout_handler)

# Configure file handler with rotation
_file_handler = logging.handlers.RotatingFileHandler(
    _LOG_FILE_PATH,
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5  # Number of backup files to keep
)
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(_formatter)
log.addHandler(_file_handler)
