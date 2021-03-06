import logging
import inspect
import numpy as np
from datetime import datetime
from pathlib import Path

LOGGING_CONFIGURED = False


def configure_file_logging(file_id):
    """
    Configures the logger to log to a file.

    :param file_id: An id to append to the file name. Useful when you run the same code but you want identifiable log files
    :return: None
    """
    global LOGGING_CONFIGURED

    np.set_printoptions(linewidth=np.inf)
    Path("./logs").mkdir(exist_ok=True)
    logging.basicConfig(filename=__get_logging_file_name__(file_id), level=logging.DEBUG)
    LOGGING_CONFIGURED = True


def log(content):
    """
    Logs the content to file. You must call configure_file_logging before using log.

    :param content: Anything that can be represented as a string
    :return: None
    """
    global LOGGING_CONFIGURED
    if LOGGING_CONFIGURED:
        logging.debug(f"{__get_caller_name()}: {content}")


def error(message="An error occurred"):
    """
    Logs the error to fil with the given message. You must call configure_file_logging before using log.

    :param message: A message to go with the error
    :return: None
    """
    global LOGGING_CONFIGURED
    if LOGGING_CONFIGURED:
        logging.exception(message)


def __get_logging_file_name__(file_id):
    """
    Composes a logging file name. It contains a timestamp followed by a file id.
    Example: 20210306113741-MyBot-2.log

    :param file_id: An id to append to the file name. Useful when you run the same code but you want identifiable log files
    :return: str
    """
    return f"logs/{datetime.now().strftime('%Y%m%d%H%M%S')}-{file_id}.log"


def __get_caller_name():
    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    return module.__name__
