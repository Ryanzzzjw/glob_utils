from enum import Enum
import os
from typing import Any, Union
import glob_utils.args.check_type 
import glob_utils.args.kwargs 
import glob_utils.log.msg_trans
import glob_utils.dialog.Qt_dialogs
import logging
import glob_utils.directory.utils

logger = logging.getLogger(__name__)

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
    json= '.json' # csv files
    png= '.png' # png files
    jpeg= '.jpeg' # csv files

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
    # root=Tk()
    # root.withdraw() # we don't want a full GUI, so keep the root window from appearing

    # # show an "Open" dialog box and return the path to the selected file
    # file_path = askopenfilename(
    #     initialdir=initialdir or os.getcwd(),
    #     filetypes=file_types or [("All files","*.*")],
    #     title=title or 'Select a file',
    #     **kwargs)
    # root.destroy()
    file_path= glob_utils.dialog.Qt_dialogs.openFileNameDialog(
        filters=file_types or [("All files","*")],
        directory=initialdir or os.getcwd(),
        title=title or 'Select a file'
    )

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
    title= kwargs.pop('title', None) # pop title
    title= title or f'Please select *{ext} files' if ext else None
    file_types=[(f"{ext}-file",f"*{ext}")] if ext else None
    file_types=kwargs.pop('file_types', file_types)
    
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
    glob_utils.args.check_type.isstring(path, raise_error)


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

    glob_utils.directory.utils.dir_exist(dir_path=dir_path, raise_error=True)
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

################################################################################
# Methods
################################################################################
def append_extension(path:str, ext:Union[str, FileExt]= None)->str:
    """ Append and or replace the extension of a path
    
    Args:
        path (str): path of the file
        ext (Union[str, FileExt]): extension to append. (e.g.: '.png')
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


def logging_file_loaded(file_path:str=None, )->None:
    """[summary]

    Args:
        file_path (str, optional): [description]. Defaults to None.
    """
    _logging_file_loaded(file_path,'LOADED')

def logging_file_saved(file_path:str=None)->None:
    """[summary]

    Args:
        file_path (str, optional): [description]. Defaults to None.
    """
    _logging_file_loaded(file_path,'SAVED')

def _logging_file_loaded(file_path:str=None, action:str= 'LOADED')->None:
    """[summary]

    Args:
        file_path (str, optional): [description]. Defaults to None.
    """
    dir_path, filename= os.path.split(file_path)
    msg=f'File: {filename} - {action}\nDirectory: {dir_path}'
    logger.info(glob_utils.log.msg_trans.highlight_msg(msg, '-'))

if __name__ == "__main__":
    from glob_utils.log.log  import main_log
    main_log()
    f=f'f {FileExt.txt}'
    print(f,  FileExt.mat )

    print(dialog_get_file())
