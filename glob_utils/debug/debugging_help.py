

import logging
from typing import Any
import logging

from numpy import ndarray

import glob_utils.log.log

logger = logging.getLogger(__name__)

def print_obj_type_dict(obj:Any)->None:
    """Print the type of the passed object,
    or log it as debug if logger exists

    Args:
        obj (Any): [description]
    """
    type_obj= type(obj)
    dict_obj = obj.__dict__ if hasattr(obj,'__dict__') else None

    msg= f'{obj=}\n{type_obj=}\n{dict_obj=}'
    if glob_utils.log.log.check_logger_exist():
        level_tmp= glob_utils.log.log.change_level_logging()
        logger.debug(msg)
        glob_utils.log.log.change_level_logging(level_tmp)
    else:
        print(msg)

def print_np(array:ndarray, shape_only= False, id="array"):

    msg= f'{id}.shape:{array.shape}' if shape_only else f'{id}:{array}\n{id}.shape:{array.shape}\ntype({id}):{type(array)}'
    if glob_utils.log.log.check_logger_exist():
        level_tmp= glob_utils.log.log.change_level_logging()
        logger.debug(msg)
        glob_utils.log.log.change_level_logging(level_tmp)
    else:
        print(msg)
    


if __name__ == '__main__':
    """"""
    from glob_utils.log.log import change_level_logging, main_log
    main_log()
    change_level_logging(logging.INFO)
    a= 2
    print_obj_type_dict(a)
