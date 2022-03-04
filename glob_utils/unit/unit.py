import re
from typing import Tuple, Union
import numpy as np

# prefixe table with the corresping exponent ( 10^exp) as key
UNIT_PREFIX = {
    -24 : 'y', # yokto
    -21 : 'z', # zepto
    -18 : 'a', # atto
    -15 : 'f', # femto
    -12 : 'p', # pico
    -9  : 'n', # nano
    -6  : 'u', # micro
    -3  : 'm', # milli
    0   : '',  # 
    3   : 'k', # kilo
    6   : 'M', # mega
    9   : 'G', # giga
    12  : 'T', # tera 
    15  : 'P', # peta
    18  : 'E', # exa
    21  : 'Z', # zetta
    24  : 'Y'  # yotta
    } 
    

# def unit_converter_str(var,format_str:str='.2f')-> str:
#     """ Convert a float in a str with a unit and a prefix .
#         such as  val=1000, default_unit = 'Hz' > '1.0 kHz'

#     Args:
#         val (float): Value to convert
#         default_unit (str): unit in which the value is expressed

#     Returns:
#         str: String with converted value and unit
#     """
#     variable = re.findall(r'[A-Za-z]+|\d+\.?\d*', var)
#     number, unit = float(variable[0]), variable[1]
#     return eng(number, unit, format_str)


def eng(x:Union[float, int], unit:str='', format_str:str='.4g')-> str:
    """Return a string representing x in an engineer friendly notation with a unit and a prefix .
       such as  val=1000, unit = 'Hz' > '1.000 kHz'

    Args:
        x (Union[float, int]): value to represent
        unit (str, optional): unit in which x is expressed. Defaults to ''.
        format_str (str, optional): format of the value. Defaults to '.4g'.

    Raises:
        TypeError: raise in case x is not an int or a float

    Returns:
        str: represention of x in an engineer friendly notation with a unit and a prefix .
    """
    
    if not isinstance(x, (int, float)):
        raise TypeError('x should be an integer or a float')

    x= float(x)
    a,exp = powerise10(x)

    if -3 < exp < 3:
        new_val,exp3= x, 0
    new_val = a * 10**(exp % 3)
    exp3 = exp - exp % 3

    if exp3 not in list(UNIT_PREFIX.keys()):
        new_val=x
        exp3= 0

    return f'{str(format(new_val, format_str))} {UNIT_PREFIX[exp3]}{unit}'

def powerise10(x:float)->Tuple[float, int]:
    """Returns a number x as a*10**exp with 0 <= a < 10

    Args:
        x (float): number to 

    Returns:
        Tuple[float, int]: a and exp
    """
    
    if x == 0:
        return 0,0
    sign= np.sign(x)
    x= np.abs(x)
    a = 1.0 * x / 10**(np.floor(np.log10(x)))
    exp = int(np.floor(np.log10(x)))
    return sign*a,exp


if __name__ == "__main__":
    from random import randint, random
    from glob_utils.log.log  import main_log

    for i in range(-30, 30):
        a= random()*10**i
        b=eng(a, 'Hz')
        print(f'{a=} >> {b}')

    main_log()

    
        