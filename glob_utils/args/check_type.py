from typing import Any



def checkinstance(inst:Any, cls:Any, raise_error:bool=True) -> bool:
    """Check if var is an instance of cls

    Args:
        var (str): variable to check
        raise_error (bool, optional): TypeError raised if set to `True`. Defaults to `False`.

    Raises:
        TypeError: raised if var is not string

    Returns:
        bool: `True` if var is a string
    """    
    is_ =isinstance(inst, cls)
    if not is_ and raise_error:
        raise TypeError(f'Wrong type of {inst=}, {type(inst)=}, expected {cls}')
    return is_


def isstring(var:Any, raise_error:bool=False) -> bool:
    """Check if var is a string

    Args:
        var (str): variable to check
        raise_error (bool, optional): TypeError raised if set to `True`. Defaults to `False`.

    Raises:
        TypeError: raised if var is not string

    Returns:
        bool: `True` if var is a string
    """    
    is_ =isinstance(var, str)
    if not is_ and raise_error:
        raise TypeError(f'String expected: {var=} is not a str')
    return is_


def isint(var:Any, raise_error:bool=False)-> bool:
    """Check if var is an integer

    Args:
        var (str): variable to check
        raise_error (bool, optional): TypeError raised if set to `True`. Defaults to `False`.

    Raises:
        TypeError: raised if var is not an integer

    Returns:
        bool: `True` if var is an integer
    """    
    is_ =isinstance(var, int)
    if not is_ and bool(raise_error):
        raise TypeError(f'Integer expected: {var=} is not an int')
    return is_


def isfloat(var:Any, raise_error:bool=False)-> bool:
    """Check if var is a float

    Args:
        var (str): variable to check
        raise_error (bool, optional): TypeError raised if set to `True`. Defaults to `False`.

    Raises:
        TypeError: raised if var is not a float

    Returns:
        bool: `True` if var is a float
    """    
    is_ =isinstance(var, float)
    if not is_ and bool(raise_error):
        raise TypeError(f'Float expected: {var=} is not a float')
    return is_

def isbool(var:Any, raise_error:bool=False)-> bool:
    """Check if var is a boolean

    Args:
        var (str): variable to check
        raise_error (bool, optional): TypeError raised if set to `True`. Defaults to `False`.

    Raises:
        TypeError: raised if var is not a boolean

    Returns:
        bool: `True` if var is a boolean
    """    
    is_ =isinstance(var, bool)
    if not is_ and bool(raise_error):
        raise TypeError(f'Boolean expected: {var=} is not a bool')
    return is_