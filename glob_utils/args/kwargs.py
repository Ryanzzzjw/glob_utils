
from typing import Any

from glob_utils.args.check_type import isstring


def kwargs_extract( kwargs:dict, key:str, default_value:Any=None)->Any:
    """Extract the value of a key contained in kwargs

    if the key is contained the corresponing value is returned, 
    otherwise an the default_value is returned

    Args:
        kwargs (dict): keywords arguments dict
        key (str): key to extract
        default_value (Any, optional): value to return in case of key is not 
        contained in kwargs. Defaults to None.

    Returns:
        Any: value extracted
    """    
    isstring(key, raise_error=True)
    return kwargs.pop(key) if key in kwargs else default_value



if __name__ == "__main__":
    """"""