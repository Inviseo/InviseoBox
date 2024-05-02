import logging

class Logger:
    def __init__(self, log_file='../inviseo.log', log_level=logging.DEBUG):
        self.log_file = log_file
        self.log_level = log_level
        
        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        
        # Create a file handler and set the logging level
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.log_level)
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
    def log_info(self, message):
        self.logger.info(message)
        
    def log_warning(self, message):
        self.logger.warning(message)
        
    def log_error(self, message):
        self.logger.error(message)
        
    def log_debug(self, message):
        self.logger.debug(message)
