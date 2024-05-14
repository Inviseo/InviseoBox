import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file='./inviseo.log', log_level=logging.DEBUG, max_bytes=1048576000, backup_count=5):

        # Remove the log file if it exists
        if os.path.exists(log_file):
            os.remove(log_file)

        self.log_file = log_file
        self.log_level = log_level

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        # Create a rotating file handler
        file_handler = RotatingFileHandler(self.log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(self.log_level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def debug(self, message):
        self.logger.debug(message)
