""" Logging Utils
usage: Import get_logger and add the following command.
logger = get_logger(__name__)
"""
import sys
import logging
import inspect
from logging.handlers import TimedRotatingFileHandler

formatter_str = "[%(asctime)s — %(filename)s:%(lineno)s — %(funcName)s() — %(levelname)s]\n  - %(message)s"

FORMATTER = logging.Formatter(formatter_str)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, logging_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
