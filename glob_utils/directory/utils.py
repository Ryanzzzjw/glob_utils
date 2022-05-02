import os

import tkinter     # from tkinter import Tk for Python 3.x
import tkinter.filedialog
import datetime

from logging import getLogger
import time
from typing import Union

logger = getLogger(__name__)


FORMAT_DATE_TIME= "%Y%m%d_%H%M%S"
FORMAT_TIME= "%Hh%Mm%Ss"

################################################################################
# Date time 
################################################################################


def get_datetime_s()->str:
    """Return actual datetime as str
    Format datetime is defined in FORMAT_DATE_TIME

    Returns:
        str: actual datetime
    """    
    _now = datetime.datetime.now()
    return _now.strftime(FORMAT_DATE_TIME)

def get_time()->float:
    """Return actual time as float

    Returns:
        float: actual time
    """    
    return time.time()

DATETIME_APPENDIX_DELIMITER= '_'

def append_date_time(string:str, datetime:str=None) -> str:
    """Append datetime to a string, if datetime is not given actual date time
    will be appended. Also if the string contains already at its end a 
    datetime, this will be replaced 

    Args:
        s (str): String to be appended
        datetime (str, optional): datetime to append. Defaults to `None`.

    Returns:
        str: appended string with a datetime  
    """    

    string,_= split_appendix_date_time(string)

    if string:
        string=f'{string}{DATETIME_APPENDIX_DELIMITER}'
    return f'{string}{datetime}' if datetime else f'{string}{get_datetime_s()}'

def split_appendix_date_time(string:str)-> tuple[str,str]:
    """Split string in a string_without_datetime and datetime_s

    If string is a datetime (eg. from get_datetime_s())
    'string_without_datetime' will return `''`

    Args:
        string (str): string to split

    Returns:
        tuple[str,str]: (string_without_datetime, datetime_s)
    """    
    length= len(get_datetime_s())
    string_without_datetime= string
    datetime_s= ''
    if len(string)>= length:
        try:
            datetime_s= string[-length:]
            datetime.datetime.strptime(datetime_s, FORMAT_DATE_TIME)
            string_without_datetime= string[:-length]
        except ValueError:
            datetime_s= ''
    if string_without_datetime and string_without_datetime[-1]==DATETIME_APPENDIX_DELIMITER:
        string_without_datetime= string_without_datetime[:-2]

    return string_without_datetime, datetime_s

################################################################################
# Paths
################################################################################

def get_POSIX_path(path:str)->str:
    return path.replace('\\','/')

################################################################################
#Directory 
################################################################################
class OpenDialogDirCancelledException(Exception):
    """"""
class DirNotFoundError(Exception):
    """"""    

def dir_exist(dir_path:str, create_auto:bool=False, raise_error:bool=False)->bool:
    """Test if a directory exist
    setting the create argument to `True` allow the automatic creation
    of the directory 

    Args:
        dir_path (str): directory path to test / create
        create_auto (bool, optional): allow the automatic creation
    of the directory if it not exist . Defaults to False.
        raise_error (bool, optional): DirNotFoundError raised if set to `True`.
        Defaults to `False`.

    Raises:
        `DirNotFoundError`: if path not a dir or not exist

    Returns:
        bool: return `True` if dir_path is an existing dir or
        if create_auto is set to `True`
    """    

    exist= os.path.isdir(dir_path)
    if not exist and raise_error:
        raise DirNotFoundError(f'"{dir_path}" - Directory not found!')
    else:
        logger.info(f'Directory: {dir_path} - Exist already')
        
    if not exist and create_auto:
        os.mkdir(dir_path)
        logger.info(f'Directory: {dir_path} - created')
        exist= True
    return exist

def mk_new_dir(dir_name:str, parent_dir:str= None )-> str:
    """Create a directory in a specified parent directory
    parent_dir is not specified the new dir will be created 
    in the current working directory (cwd)
    Args:
        dir_name (str): name of the new directory to create
        parent_dir (str, optional): . Defaults to None.

    Returns:
        [str]: the path of the created directory
    """    
    if not parent_dir:
        parent_dir=os.getcwd()

    dir_exist(parent_dir, create_auto=True) #create if not exist

    new_dir_path= os.path.join(parent_dir, dir_name)
    dir_exist(new_dir_path, create_auto=True) #create if not exist

    return new_dir_path

def mk_dir(dir_path:str)-> str:
    """
    Create a directory

    Args:
        dir_path (str): name of the new directory to create
        parent_dir (str, optional): . Defaults to None.

    Returns:
        [str]: the path of the created directory
    """    
    dir_exist(dir_path, create_auto=True) #create if not exist

    return dir_path

def get_dir(title:str='Select a directory', initialdir:str=None, raise_error:bool=False)->Union[str, None]:
    """Open an explorer dialog for selection of a directory

    Args:
        title (str, optional): title of the Dialog . 
        Defaults to 'Select a directory'.
        initialdir (str, optional): path of initial directory for the 
        explorer dialog. Defaults to None.
        raise_error (bool, optional): Set to True to raise 
        OpenDialogDirCancelledException, otherwise only log will be given out.
        Default to False
    Raises:
        OpenDialogDirCancelledException: when user cancelled the dialog 

    Returns:
        str: a directory path selected by a user if success otherwise return None if raise_error is False
    """    
    
    # Tk().withdraw()
    root=tkinter.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing

    # show an "Open" dialog box and return the path to the selected directory
    dir_path = tkinter.filedialog.askdirectory(
        initialdir=initialdir or os.getcwd(),
        title= title)
    root.destroy()
    if dir_path :
        return dir_path    
    msg= 'Open dialog box for directory selection - Cancelled'
    logger.info(f"{msg}")
    if raise_error:
        raise OpenDialogDirCancelledException(msg)
    return None


if __name__ == "__main__":
    from glob_utils.log.log  import change_level_logging, main_log
    import logging
    main_log()
    change_level_logging(logging.DEBUG)

    s=get_datetime_s()
    print(s)
    print(split_appendix_date_time(s))


    