import re
from tokenize import String
import numpy as np

def unit_converter(var: any):
    """ This is the main function of unit conversion.

    Args:
        var (any): 1. value correspoding to the non-prefix unit
                   2. including both value and non-prefix unit (e.g. 100A or 100 A)

    Returns:
        _type_: converted value and unit
    """
    if isinstance(var, (int, float)):
        number = float(var)
        output = unit_converter_value(number)
    elif isinstance (var, str):
        variable = re.findall(r'[A-Za-z]+|\d+\.?\d*', var)
        number, default_unit = float(variable[0]), variable[1]
        output = unit_converter_str(number, default_unit)
        
    return output
    

def unit_converter_str(val: float, default_unit: str):
    """ This function is used to convert the input including both value and non-prefix unit .

    Args:
        val (float): _description_
        default_unit (str): _description_

    Returns:
        _type_: String with converted value and unit
    """
    unit_prefix = {-9: 'n', -6: 'u', -3: 'm', 0: '', 3: 'k', 6: 'M', 9: 'G'}
    
    exponent = np.floor(np.log10(np.abs(val))).astype(int)
    if exponent < 3 and exponent > -3:
        output = str(val) + ' ' + default_unit
    
    elif exponent >= 3:
        
        if exponent % 3  == 0:
            output = str(val / (1000 **(exponent/3))) + ' ' + unit_prefix[exponent] + default_unit
        else:
            output = str(format(val / (1000 **(exponent//3)), '.2f')) + ' ' + unit_prefix[exponent - exponent % 3] + default_unit
    
    else:
        if exponent % 3 == 0:
            output = str(val * (1000**(np.abs(exponent)/3))) + ' ' + unit_prefix[exponent] + default_unit
        else:
            output = str(format((val * (1000**(np.abs(exponent)//3))), '.2f')) + ' ' + unit_prefix[exponent + np.abs(exponent) % 3] + default_unit     
        
    return output

def unit_converter_value(val: float):
    """ This function is used to convert the input including only value

    Args:
        val (float): _description_

    Returns:
        _type_: String with converted value and new prefix
    """
    
    unit_prefix = {-9: 'n', -6: 'u', -3: 'm', 0: '', 3: 'k', 6: 'M', 9: 'G'}
    
    exponent = np.floor(np.log10(np.abs(val))).astype(int)
    if exponent < 3 and exponent > -3:
        output = val
    
    elif exponent >= 3:
        
        if exponent % 3  == 0:
            output = str(val / (1000 **(exponent/3))) + ' ' + unit_prefix[exponent] 
        else:
            output = str(format(val / (1000 **(exponent//3)), '.2f')) + ' ' + unit_prefix[exponent - exponent % 3] 
    
    else:
        if exponent % 3 == 0:
            output = str(val * (1000**(np.abs(exponent)/3))) + ' ' + unit_prefix[exponent] 
        else:
            output = str(format((val * (1000**(np.abs(exponent)//3))), '.2f')) + ' ' + unit_prefix[exponent + np.abs(exponent) % 3]   
        
    return output


if __name__ == "__main__":
    from glob_utils.log.log  import main_log
    main_log()
    
    print(unit_converter('1000 Hz'))
    print(unit_converter('0.0000001A'))
    print(unit_converter('0.00001A')) 
    print(unit_converter('1000000 Hz'))
    print(unit_converter('50 A'))
    print(unit_converter(1000))
    print(unit_converter(0.0000001))
    print(unit_converter(0.00001))
    print(unit_converter(1000000))
    print(unit_converter(50))
    
    
        