from enum import Enum
import os
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askopenfilenames
import pickle
import json
import datetime
from typing import Any, Union
from glob_utils.args.check_type import isstring
from glob_utils.args.kwargs import kwargs_extract
from glob_utils.log.msg_trans import highlight_msg

import scipy.io.matlab.mio





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
    csv= '.csv' # csv files

    def __repr__(self):
      return self.value

    def __str__(self):
        return str(self.value)

################################################################################
# Dialog
################################################################################
class OpenDialogFileCancelledException(Exception):
    """Raised when User close UI dialog to abort or terminate selection"""
class DataLoadedNotCompatibleError(Exception):
    """Raised if the Data contained in a file does not correspond"""
class EmptyFileError(Exception):
    """Raised if a File is Empty"""

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
    root=Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing

    # show an "Open" dialog box and return the path to the selected file
    file_path = askopenfilename(
        initialdir=initialdir or os.getcwd(),
        filetypes=file_types or [("All files","*.*")],
        title=title or 'Select a file',
        **kwargs)
    root.destroy()

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
    title= kwargs_extract(kwargs, 'title', None) # pop title
    title= title or f'Please select *{ext} files' if ext else None
    file_types=[(f"{ext}-file",f"*{ext}")] if ext else None
    file_types=kwargs_extract(kwargs, 'file_types', file_types)
    
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


def search_for_file_with_ext(dir_path:str, ext:Union[str, FileExt]=None) -> list[str]:
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
    file_names = list(os.listdir(dir_path))
    if ext:
        file_names = [file for file in os.listdir(dir_path) 
            if is_file_with_ext(path= os.path.join(dir_path, file), ext= ext)
        ]
    if not file_names: # if no files are contains
        raise FileNotFoundError(f'No {ext}-file found in {dir_path=}')

    return file_names

def find_file(filename:str=None, dir_path:str=None)-> Union[list[str], None]:
    """ Scan dir_path to find files with filename

    Args:
        filename (str): filename to search for
        dir_path (str): directory where to search

    Raises:
        FileNotFoundError: raised if the filname not found

    Returns:
        Union[list[str], None]: return a list of the filepath
        or None if nothing has been found
    """    
    if not filename or not dir_path: 
        logger.error(f'cannot find file "{filename}" in: {dir_path=} ...')
        return None
    logger.info(f'Start searching for file "{filename}" in: {dir_path=} ...')
    file_paths= [
        os.path.join(root, filename)
        for root, _, files in os.walk(dir_path)
        if filename in files
    ]
    logger.info('Stop searching for file ...')
    logger.info(f'files found: {file_paths}')
    if not file_paths: # if no files are contains
        raise FileNotFoundError(f'File "{filename}" not found in {dir_path=}')
    return file_paths

# def find_all(filename:str, path:str)->list[str]: NOT USED
#     """ Scan a path and search for a filename

#     Args:
#         name (str): name of the file to found
#         path (str): [description]

#     Returns:
#         list[str]: list of 
#     """
#     return [
#         os.path.join(root, filename)
#         for root, dirs, filenames in os.walk(path)
#         if filename in filenames
#     ]

################################################################################
# Save/Load pkl files
################################################################################
def save_as_pickle(file_path:str, obj:Any)->None:
    """Save an object in a pkl-file

    Args:
        file_path (str): saving path
        obj (Any): object to save
    """
    file_path= append_extension(file_path, FileExt.pkl)
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)

def load_pickle(file_path:str, obj:Any=None)->Any:
    """Load an Object out of an pkl-file

    Args:
        file_path (str): pkl-file to load
        obj (Any, optional): Object to update. Defaults to None.

    Returns:
        Any: loaded object or the passed object with updated attributes
    """
    is_file_with_ext(file_path, FileExt.pkl)
    with open(file_path, 'rb') as file:
        loaded_obj = pickle.load(file)
    logging_file_loaded(file_path)
    if not obj:
        return loaded_obj
    set_existing_attrs(obj, loaded_obj)
    return obj

def load_pickle_app(file_path:str, obj:Any=None)->Any:
    """Load an Object out of an pkl-file (with EmptyFileError)

    Args:
        file_path (str): pkl-file to load
        obj (Any, optional): Object to update. Defaults to None.

    Raises:
        EmptyFileError: if file is an empty file

    Returns:
        Any: loaded object or the passed object with updated attributes

    """

    if os.path.getsize(file_path) == 0:
        raise EmptyFileError(f'{file_path} - File empty!')

    return load_pickle(file_path, obj)


    # for key in class2upload.__dict__.keys():
    #         setattr(class2upload, key, getattr(newclass,key))

################################################################################
# Save/Load txt files with json data
################################################################################
def save_as_txt(file_path:str, obj:Any)->None:
    """Save an object in a txt-file

    if obj 
        (str)  -> line[0] = obj
        (list) -> line[i] = obj[i] (item_i)
        (dict) -> line[0] ='Dictionary form:'
                  line[1] = json of the dict
                  line[5] = Single attributes:' # list attrs for better readbility
                  line[6:] = 'key= value'
        (cls) -> line[0] ='Dictionary form:'
                  line[1] = json of the cls.__dict__
                  line[5] = Single attributes:' # list attrs for better readbility
                  line[6:] = 'key= value'
        
    Args:
        file_path (str): saving path
        obj (Any): object to save
    """
    file_path= append_extension(file_path, FileExt.txt)
    lines = []
    if isinstance(obj,str):
        lines.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            lines.append(f'{item}')
    elif isinstance(obj, dict):
        lines.append('Dictionary form:')
        lines.append(json.dumps(obj))
        lines.append('\n\nSingle attributes:')
        lines.extend([f'{key} = {obj[key]},' for key in obj ])      
    else:
        tmp_dict= obj.__dict__
        lines.append('Dictionary form:')
        lines.append(json.dumps(obj.__dict__))
        lines.append('\n\nSingle attributes:')
        single_attrs= [f'{key} = {tmp_dict[key]}' for key in obj.__dict__ ]
        single_attrs= [ attr if len(attr)< 200 else f'{attr[:200]}...' for attr in single_attrs]
        lines.extend(single_attrs)

    with open(file_path, 'w') as file:
        [ file.write(f'{line}\n') for line in lines ]


def read_txt(file_path:str)-> Any:
    """Load a txt file with json data

    Args:
        file_path (str): file to load

    Returns:
        Any: return dict of the json saved data if found. None otherwise
    """
    is_file_with_ext(file_path, FileExt.txt)
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
def save_as_mat(file_path:str, data:dict)->None:
    """Save data in a mat-file

    Args:
        file_path (str): saving path
        data (dict): dictionary to save
    """

    if not isinstance(data, dict):
        logger.error(f'Saving of {data=} in mat file - failed, data should be a dict')
        return
    scipy.io.matlab.mio.savemat(file_path,data)

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

    if not check_file(file_path, FileExt.mat):
        return None
    file = scipy.io.matlab.mio.loadmat(file_path)
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
# Save/Load csv files
################################################################################
def save_as_csv(file_path:str, data:dict)->None:
    """Save data in a csv-file

    Args:
        file_path (str): saving path
        data (dict): dictionary to save
    """

    #TODO

def load_csv(file_path:str, logging:bool= True)-> dict:
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

    if not check_file(file_path, FileExt.csv):
        return None
    var = {}
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

def set_existing_attrs(old_obj:Any, new_obj:Any)->None:
    """[summary]

    Args:
        old_obj (Any): [description]
        new_obj (Any): [description]
    """
    for key in new_obj.__dict__.keys():
        if key in old_obj.__dict__.keys():
            setattr(old_obj,key, getattr(new_obj,key))

def set_attributes(old_obj:Any, new_obj:Any) -> None:
    """[summary]

    Args:
        old_obj (Any): [description]
        new_obj (Any): [description]

    Raises:
        DataLoadedNotCompatibleError: [description]
    """
    if not isinstance(new_obj, type(old_obj)):
        raise DataLoadedNotCompatibleError(f'loaded data type{type(new_obj,)}, expected type {type(old_obj)}')

    for key in new_obj.__dict__.keys():
        setattr(old_obj, key, getattr(new_obj,key))

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



def logging_file_loaded(file_path:str=None)->None:
    """[summary]

    Args:
        file_path (str, optional): [description]. Defaults to None.
    """
    dir_path, filename= os.path.split(file_path)
    msg=f'Loading file: {filename}\n(dir: ...{dir_path})'
    logger.info(highlight_msg(msg))

if __name__ == "__main__":
    from glob_utils.log.log  import main_log
    main_log()
    f=f'f {FileExt.txt}'
    print(f,  FileExt.mat )

    print(find_file())
