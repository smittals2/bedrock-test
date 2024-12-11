# logger_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_file='app.log', log_level=logging.INFO):
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_path = os.path.join(log_dir, log_file)

    # Create a formatter
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # Setup file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add the file handler
    root_logger.addHandler(file_handler)

    return root_logger
