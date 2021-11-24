#!/usr/bin/env python3

import logging
import sys
import os

from glob_utils.args.check_type import isint, isstring
from glob_utils.files.files import FileExt, append_ext

logger = logging.getLogger()

# http://stackoverflow.com/a/24956305/1076493
# filter messages lower than level (exclusive)
class MaxLevelFilter(logging.Filter):
    """ Define a filter for logging msg
    >> limit msg < max level
    """    
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record:logging.LogRecord)-> bool:
        return record.levelno < self.max_level

MAX_LOG_MSG_LENGTH= 80

def highlight_msg(msg:str, symbol:str='#')->str:
    """Add a continious line of symbol before and after a message to highlight it
    eg.:
    ############################################################################
    msg
    ############################################################################

    Args:
        msg (str): msg to highlight
        symbol (str, optional): symbol for highlighting. Defaults to '#'.

    Returns:
        str: highlighted message (at least 3 lines)
    """    
    isstring(msg, raise_error=True)
    isstring(symbol, raise_error=True)

    sym= symbol*MAX_LOG_MSG_LENGTH
    sym = trunc_msg(sym, MAX_LOG_MSG_LENGTH) # in case that sym is not a single char
    return f'\n{sym}\n{msg}\n{sym}'    

def trunc_msg(msg:str, max_length:int=MAX_LOG_MSG_LENGTH, trunc_end:bool=True)->str:
    """Truncate a msg to a max_length

    Args:
        msg (str): message to truncate
        max_length (int, optional): [description]. Defaults to MAX_LOG_MSG_LENGTH.
        trunc_end (bool, optional): if set to `True` the end of the message is truncated. Defaults to `True`.

    Returns:
        [str]: truncated message
    """    
    isstring(msg, raise_error=True)
    isint(max_length, raise_error=True)
    
    if len(msg)< max_length: 
        return msg
    return msg[:max_length] if trunc_end else msg[-max_length:]

def log_file_loaded(file_path:str=None):
    dir_path, filename= os.path.split(file_path)
    msg=f'Loading file: {filename}\n(dir: ...{dir_path})'
    logger.info(highlight_msg(msg))

def main_log(logfile:str='debug.log')->None:
    """Set the globals logging parameters

    Args:
        logfile (str, optional): path for the logging file. Defaults to 'debug.log'.
    """    
    # redirect messages to either stdout or stderr based on loglevel
    # stdout < logging.WARNING <= stderr
    format_long = logging.Formatter('%(asctime)s %(levelname)s [%(threadName)s] [%(module)s]: %(message)s')
    format_short = logging.Formatter('%(levelname)s [%(module)s]: %(message)s')
    
    logging_out_h = logging.StreamHandler(sys.stdout)

    logging_err_h = logging.StreamHandler(sys.stderr)
    logging_file_h = logging.FileHandler(append_ext(logfile, FileExt.log))
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
    
def change_level_logging(level:int=logging.DEBUG)->None:
    """Modify the logging level

    Args:
        level (int, optional): new logging level. Defaults to logging.DEBUG.
    """    
    logger.setLevel(level)

if __name__ == '__main__':
    main_log()
    msg = 'Training results will be found in : huirhguihruhguher'
    logger.info(highlight_msg(msg))