import os
import logging
import pytest
from Logger import Logger
from logging.handlers import RotatingFileHandler

@pytest.fixture
def logger():
    return Logger(log_file='test_inviseo.log', log_level=logging.DEBUG, max_bytes=1000, backup_count=5)

def test_logger_creation(logger):
    assert logger.logger is not None
    assert logger.logger.level == logging.DEBUG
    assert len(logger.logger.handlers) == 2

# def test_logger_file_handler(logger):
#     file_handler = next(handler for handler in logger.logger.handlers if isinstance(handler, RotatingFileHandler))
#     assert file_handler is not None
#     assert file_handler.level == logging.DEBUG
#     assert os.path.abspath(file_handler.baseFilename) == os.path.abspath('test_inviseo.log')

def test_logger_console_handler(logger):
    console_handler = next(handler for handler in logger.logger.handlers if isinstance(handler, logging.StreamHandler))
    assert console_handler is not None
    assert console_handler.level == logging.DEBUG

def test_logger_info(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.info("This is an info message")
        assert "This is an info message" in caplog.text

def test_logger_warning(logger, caplog):
    with caplog.at_level(logging.WARNING):
        logger.warning("This is a warning message")
        assert "This is a warning message" in caplog.text

def test_logger_error(logger, caplog):
    with caplog.at_level(logging.ERROR):
        logger.error("This is an error message")
        assert "This is an error message" in caplog.text

def test_logger_debug(logger, caplog):
    with caplog.at_level(logging.DEBUG):
        logger.debug("This is a debug message")
        assert "This is a debug message" in caplog.text

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code to run before each test
    yield
    # Code to run after each test
    if os.path.exists('test_inviseo.log'):
        os.remove('test_inviseo.log')
