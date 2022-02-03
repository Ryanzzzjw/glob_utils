

import logging
from typing import Any
from logging import debug, getLogger

from glob_utils.log.log import change_level_logging, check_logger_exist, main_log
logger = getLogger(__name__)

def print_obj_type_dict(obj:Any)->None:
    """Print the type of the passed object,
    or log it as debug if logger exists

    Args:
        obj (Any): [description]
    """
    type_obj= type(obj)
    dict_obj = obj.__dict__ if hasattr(obj,'__dict__') else None

    msg= f'{obj=}\n{type_obj=}\n{dict_obj=}'
    if check_logger_exist():
        level_tmp= change_level_logging()
        logger.debug(msg)
        change_level_logging(level_tmp)
    else:
        print(msg)


if __name__ == '__main__':
    """"""
    # main_log()
    change_level_logging(logging.INFO)
    a= 2
    print_obj_type_dict(a)
