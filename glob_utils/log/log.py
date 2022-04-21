#!/usr/bin/env python3

import logging
import sys
from typing import Union

# import coloredlogs

from glob_utils.file.utils import FileExt, append_extension

logger = logging.getLogger()

# http://stackoverflow.com/a/24956305/1076493
# filter messages lower than level (exclusive)

################################################################################
# Logging setting
################################################################################

LOG_LEVELS = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING}


class MaxLevelFilter(logging.Filter):
    """ Define a filter for logging msg
    >> limit msg < max level
    """    
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record:logging.LogRecord)-> bool:
        return record.levelno < self.max_level


def main_log(logfile:str='debug.log')->None:
    """Set the globals logging parameters

    Args:
        logfile (str, optional): path for the logging file. Defaults to 'debug.log'.
    """    
    # redirect messages to either stdout or stderr based on loglevel
    # stdout < logging.WARNING <= stderr
    format_long = logging.Formatter('%(asctime)s %(levelname)s [%(threadName)s] [%(module)s]: %(message)s')
    
    format_short = logging.Formatter('%(levelname)s [%(module)s]: %(message)s') #coloredlogs.ColoredFormatter
    
    logging_out_h = logging.StreamHandler(sys.stdout)

    logging_err_h = logging.StreamHandler(sys.stderr)
    logging_file_h = logging.FileHandler(append_extension(logfile, FileExt.log))
    logging_out_h.setFormatter(format_short)
    logging_err_h.setFormatter(format_short)
    logging_file_h.setFormatter(format_long)

    logging_out_h.addFilter(MaxLevelFilter(logging.WARNING))
    logging_out_h.setLevel(logging.DEBUG)
    logging_err_h.setLevel(logging.WARNING)
    logging_file_h.setLevel(logging.DEBUG)

    # root logger, no __name__ as in submodules further down the hierarchy
    global logger
    
    logger.addHandler(logging_out_h)
    logger.addHandler(logging_err_h)
    logger.addHandler(logging_file_h)
    logger.setLevel(logging.DEBUG)
    logger.hasHandlers()

def check_logger_exist()-> bool:
    """Check if the logger exist
    (if handlers were defined)

    Returns:
        bool: `True` if logger exist/has handlers, otherwise `False`
    """
    return logger.hasHandlers()
    
def change_level_logging(level:Union[int,str]=logging.DEBUG)->int:
    """Modify the logging level

    Args:
        level (Union[int,str], optional): new logging level. Defaults to logging.DEBUG.

    Returns:
        int: level before change
    """
    if isinstance(level, str):
        level = LOG_LEVELS[level]
    actual_level= logger.getEffectiveLevel()
    logger.setLevel(level)
    return actual_level

def list_levels()->list[str]:
    return list(LOG_LEVELS.keys())

if __name__ == '__main__':
    main_log()
    msg = 'Training results will be found in : huirhguihruhguher'
    logger.debug('Info msg')
    logger.info('Info msg')
    logger.warning('Info msg')
    logger.error('Info msg')
    logger.critical('Info msg')