from enum import Enum
import os
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askopenfilenames
import pickle
import json
import datetime
from typing import Any, Union
from glob_utils.args.check_type import isstring
from glob_utils.log.msg_trans import highlight_msg





from logging import debug, getLogger

from glob_utils.pth.path_utils import dir_exist

logger = getLogger(__name__)

################################################################################
# File ext managed here
################################################################################
class FileExt(Enum):
    """Set all files extensions used

    to get the str-value use eg.:
    FileExt.mat.value
    f'{FileExt.mat}'
    print(FileExt.mat)
    
    Args:
        Enum ([type]): [description]
    """
    mat= '.mat' # matlab files
    pkl= '.pkl' # pickle files
    txt= '.txt' # text files
    log= '.log' # log files

    def __repr__(self):
      return self.value

    def __str__(self):
        return str(self.value)

################################################################################
# Dialog
################################################################################
class OpenDialogFileCancelledException(Exception):
    """"""
class DataLoadedNotCompatibleError(Exception):
    """"""
class EmptyFileError(Exception):
    """"""

def dialog_get_file(
    file_types:list=None,
    initialdir:str=None,
    title:str=None,
    **kwargs) -> str:
    """Open dialog box for file selection from user

    Args:
        file_types (list, optional): file filter for Open dialog. 
        Defaults to `None` ([("All files","*.*")]).
        initialdir (str, optional): initial directory for Open dialog. 
        Defaults to `None` (set to cwd).
        title (str, optional): title of the Open dialog. 
        Defaults to `None`("Select a file").
        **kwargs (optional): additional keywords of 
        tkinter.filedialog.askopenfilename can be transmited


    Raises:
        `OpenDialogFileCancelledException`: raised if the dialog box is closed 
        from the user

    Returns:
        [str]: path of the file selected
    """    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    # show an "Open" dialog box and return the path to the selected file
    file_path = askopenfilename(
        initialdir=initialdir or os.getcwd(),
        filetypes=file_types or [("All files","*.*")],
        title=title or 'Select a file',
        **kwargs)

    if not file_path:
        raise OpenDialogFileCancelledException(
            'Open dialog box for file selection - Cancelled')

    return file_path
 
def dialog_get_file_with_ext(
    ext:Union[str,FileExt]=None,
    **kwargs)-> str:
    """Open dialog box for file selection from user (with special extension)

    Args:
        ext (Union[str,FileExt], optional): [description].
        Defaults to `None` (Similar to `dialog_get_file`).
        **kwargs (optional): additional keywords of 
        dialog_get_file can be transmited eg.:
            file_types (list, optional): file filter for Open dialog. 
            initialdir (str, optional): initial directory for Open dialog. 
            title (str, optional): title of the Open dialog.
    Raises:
        `OpenDialogFileCancelledException`: raised if the dialog box is closed 
        from the user
        `WrongFileExtError`: if path does not a file or not exist
        `NotFileError`: if path not a file or not exist

    Returns:
        [str]: path of the file selected
    """ 
    title= kwargs.pop('title') if 'title' in kwargs else None # pop title
    title= title or f'Please select *{ext} files' if ext else None
    file_types=[(f"{ext}-file",f"*{ext}")] if ext else None
    file_path =dialog_get_file(
        title=title,
        file_types=file_types,
        **kwargs)    
    check_file(file_path, ext=ext, raise_error=True)
    return file_path

class WrongFileExtError(Exception):
    """"""
class NotFileError(Exception):
    """"""

def check_file(path:str, ext:Union[str, FileExt]=None, raise_error:bool=False)-> Union[str, None]:
    """Check if path correspond to a file with a specific extension/type

    Args:
        path (str): path to check
        ext (Union[str, FileExt]): extension to check. 
        Defaults to `None` (no extension checking)
        raise_error (bool, optional): Errors raised if set to `True`.
        Defaults to `False` (only logging).

    Raises:
        `WrongFileExtError`: if path does not a file or not exist
        `NotFileError`: if path not a file or not exist

    Returns:
        Union[str, None]: the "checked" path of a file or None
    """    

    return is_file_with_ext(path, ext, raise_error)

def is_file(path:str, raise_error:bool=False)-> Union[str, None]:
    """Check if path correspond to a file

    Args:
        path (str): path to check
        raise_error (bool, optional): NotFileError raised if set to `True`.
        Defaults to `False` (only logging).

    Raises:
        `NotFileError`: if path not a file or not exist

    Returns:
        Union[str, None]: the "checked" path of a file or None
    """
    if path is None:
        return None
    isstring(path, raise_error)


    if not os.path.isfile(path):
        error_msg= f'"{path=}" does not exist or is not a file!'
        logger.warning(error_msg)
        if raise_error:
            raise NotFileError(error_msg)
        return None
    return path 

def is_file_with_ext(path:str, ext:Union[str, FileExt]= None, raise_error:bool=False)-> Union[str, None]: 
    """Check if path correspond to a file with a specific extension/type

    Args:
        path (str): path to check
        ext (Union[str, FileExt]): extension to check. 
        Defaults to `None` (no extension checking)
        raise_error (bool, optional): Errors raised if set to `True`.
        Defaults to `False` (only logging).

    Raises:
        `WrongFileExtError`: if path does not a file or not exist
        `NotFileError`: if path not a file or not exist

    Returns:
        Union[str, None]: the "checked" path of a file or None
    """       
    path = is_file(path, raise_error) #check is a file
    if path is None: # if not file return None 
        return None

    if ext is None: # do not check ext
        return path

    # ext checking
    _, file_ext = os.path.splitext(path)
    if file_ext != f'{ext}':
        error_msg= f'"{path=}"- is not a {ext}-file!'
        logger.error(error_msg)
        if raise_error:
            raise WrongFileExtError(error_msg)
        return None
    return path


def search_for_file_with_ext(dir_path:str, ext:Union[str, FileExt]=None)-> list[str]:
    """List the names (not path) of files contained in a directory dir
    with a specific extension (if given)

    Args:
        dir_path (str): search directory path
        ext (Union[str, FileExt], optional): file extension to search.
        Defaults to `None`, all files will be listed.

    Raises:
        FileNotFoundError: raised if no files are to found in the dir

    Returns:
        list[str]: List of filenames contained in a dir 
    """    

    dir_exist(dir_path=dir_path, raise_error=True)
    file_names = [file for file in os.listdir(dir_path)]
    if ext:
        file_names = [file for file in os.listdir(dir_path) 
            if is_file_with_ext(path= os.path.join(dir_path, file), ext= ext)
        ]
    if not file_names: # if no files are contains
        raise FileNotFoundError(f'No {ext}-file found in {dir_path=}')

    return file_names
    
################################################################################
# Save/Load pkl files
################################################################################
def save_as_pickle(file_path, obj, append_ext=True)->None:
    file_path= append_extension(file_path, FileExt.pkl) if append_ext else file_path
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)

def load_pickle(file_path, obj=None)->Any:
    with open(file_path, 'rb') as file:
        loaded_obj = pickle.load(file)
    logging_file_loaded(file_path)
    if not obj:
        return loaded_obj
    set_existing_attrs(obj, loaded_obj)
    return obj

def load_pickle_app(file_path, obj=None):
    """[summary]

    Args:
        filename ([type]): [description]
        class2upload ([type], optional): [description]. Defaults to None.
        verbose (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """
    if os.path.getsize(file_path) == 0:
        raise EmptyFileError(f'{file_path} - File empty!')

    with open(file_path, 'rb') as file:
        loaded_obj = pickle.load(file)
    logging_file_loaded(file_path)
    if not obj:
        return loaded_obj
    set_attributes(obj,loaded_obj)
    return obj


    # for key in class2upload.__dict__.keys():
    #         setattr(class2upload, key, getattr(newclass,key))

################################################################################
# Save/Load txt files
################################################################################
def save_as_txt(file_path, obj, append_ext=True)->None:
    file_path= append_extension(file_path, FileExt.txt) if append_ext else file_path
    
    list_of_strings = []
    if isinstance(obj,str):
        list_of_strings.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            list_of_strings.append(f'{item}')
    elif isinstance(obj, dict):
        list_of_strings.append('Dictionary form:')
        list_of_strings.append(json.dumps(obj))
        list_of_strings.append('\n\nSingle attributes:')
        list_of_strings.extend([f'{key} = {obj[key]},' for key in obj ])      
    else:
        tmp_dict= obj.__dict__
        list_of_strings.append('Dictionary form:')
        list_of_strings.append(json.dumps(obj.__dict__))
        list_of_strings.append('\n\nSingle attributes:')
        single_attrs= [f'{key} = {tmp_dict[key]}' for key in obj.__dict__ ]
        single_attrs= [ attr if len(attr)< 200 else f'{attr[:200]}...' for attr in single_attrs]
        list_of_strings.extend(single_attrs)

    with open(file_path, 'w') as file:
        [ file.write(f'{st}\n') for st in list_of_strings ]

def read_txt(file_path:str)-> Any:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    logger.debug(f'{lines=}')
    if not lines:
        return None
    if 'Dictionary form:' in lines[0]:
        out= json.loads(lines[1].replace('\n', ''))
        logging_file_loaded(file_path)
        return out
    

################################################################################
# Save/Load mat files
################################################################################
def save_as_mat(file_path:str, data:dict, append_ext:bool=True)->None:

    from scipy.io.matlab.mio import savemat
    if not isinstance(data, dict):
        logger.error(f'Saving of {data=} in mat file - failed, data should be a dict')
        return
    savemat(file_path,data, appendmat=append_ext)

def load_mat(file_path:str, logging:bool= True)-> dict:
    """Load a matlab mat-file.

    All variables contained in a mat-file (except the private var) are  
    return in a dictionnary

    Args:
        file_path (str): path of matlab mat-file to load
        logging (bool, optional): if set to 'True' logging will be recorded
            info: file loaded info
            debug: show the keys of the returned dict

    Returns:
        dict: variables contained in the mat-file
    """    
    from scipy.io.matlab.mio import loadmat
    if not check_file(file_path, FileExt.mat):
        return
    file = loadmat(file_path)
    var = {key: file[key] for key in file.keys() if "__" not in key}
    if logging:
        logging_file_loaded(file_path)
        # list_var_loaded= [str(k)+' : '+str(v) for k , v in var.items()]
        # list_var_loaded='\n'.join(list_var_loaded)
        logger.debug(f'Loaded keys:{list(var.keys())}')
    return var



# def load_file(file_path:str='', ext:Union[str, FileExt]=FileExt.mat, **kwargs):
#     """load all variables contained in a mat file in a dictionnary,
#     return the dict and the file_path (in case of selection by user)"""
#     _ , file_path= get_file_dir_path(file_path, ext=ext, **kwargs)
    
#     return var, file_path


################################################################################
# Methods
################################################################################
def append_extension(path:str, ext:Union[str, FileExt]= None)->str:
    """ Append and or replace the extension of a path
    
    Args:
        path (str): path of the file
        ext (Union[str, FileExt]): extension to append. 
        Default to `None` (no appending)

    Returns:
        str: path with appended extension
    """    
    return f'{os.path.splitext(path)[0]}{ext}' if ext is not None else path

def set_existing_attrs(obj, new_obj)->None:
    for key in new_obj.__dict__.keys():
        if key in obj.__dict__.keys():
            setattr(obj,key, getattr(new_obj,key))

def set_attributes(obj,new_obj) -> None:
    if not isinstance(new_obj, type(obj)):
        raise DataLoadedNotCompatibleError(f'loaded data type{type(new_obj,)}, expected type {type(obj)}')

    for key in new_obj.__dict__.keys():
        setattr(obj, key, getattr(new_obj,key))

# def log_saving(filename, class2save= None):
#     if hasattr(class2save, 'type'):
#         logger.info(f'{class2save.type} saved in : ...{filename[-50:]}')
#     else:
#         logger.info(f'Some data were saved in : ...{filename[-50:]}')
# def log_loading(filename, classloaded= None):
#     if hasattr(classloaded, 'type'):
#         logger.info(f'\n{classloaded.type} object loaded from : ...{filename[-50:]}')
#     else:
#         logger.info(f'\nSome data were loaded from : ...{filename[-50:]}')



def logging_file_loaded(file_path:str=None):
    dir_path, filename= os.path.split(file_path)
    msg=f'Loading file: {filename}\n(dir: ...{dir_path})'
    logger.info(highlight_msg(msg))

if __name__ == "__main__":
    from glob_utils.log.log  import main_log
    main_log()
    f=f'f {FileExt.txt}'
    print(f,  FileExt.mat )