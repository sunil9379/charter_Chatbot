import logging
import os

def setup_log(log_file,level=logging.INFO,logger_name=None):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name or __name__)
    logger.setLevel(level)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)

    return logger