from enum import Enum
import os
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
import pickle
import json
import datetime
from typing import Any, Union

from logging import getLogger

logger = getLogger(__name__)

################################################################################
# File ext managed here
################################################################################
class FileExt(Enum):
    """Set all files ext used

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

    def __repr__(self):
      return self.value

    def __str__(self):
        return str(self.value)

################################################################################
# Dialog
################################################################################
class OpenDialogFileCancelledException(Exception):
    """"""
class LoadCancelledException(Exception):
    """"""
class WrongFileTypeSelectedError(Exception):
    """"""

def get_file(file_types=[("All files","*.*")], initialdir:str=None, title:str= '', split:bool=True, **kwargs):
    """used to get select files using gui (multiple types of file can be set!)

    Args:
        filetypes (list, optional): [description]. Defaults to [("All files","*.*")].
        path ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    # show an "Open" dialog box and return the path to the selected file
    file_path = askopenfilename(
        initialdir=initialdir or os.getcwd(),
        filetypes=file_types,
        title=title, **kwargs, )

    if not file_path:
        raise OpenDialogFileCancelledException()

    return os.path.split(file_path) if split else file_path
 

def get_file_dir_path( file_path:str='', ext:str=FileExt.txt.value, **kwargs):
    """

    Args:
        file_path (str, optional): [description]. Defaults to ''.
        ext ([type], optional): [description]. Defaults to const.EXT_MAT.

    Raises:
        LoadCancelledException: [description]
        WrongFileTypeSelectedError: [description]

    Returns:
        [type]: [description]
    """
    title= kwargs.pop('title') if 'title' in kwargs else None # pop title

    file_path= verify_file(file_path, ext=ext)        
    if not file_path:
        try: 
            file_path =get_file(
                title=title or f'Please select *{ext} files',
                file_types=[(f"{ext}-file",f"*{ext}")],
                split=False,**kwargs)
        except OpenDialogFileCancelledException:
            raise LoadCancelledException('Loading aborted from user')
    dir_path=os.path.split(file_path)[0]

    if not verify_file(file_path, ext=ext):
        raise WrongFileTypeSelectedError('User selected a file with wrong extension!')

    return dir_path , file_path

def verify_file(file_path:str, ext:Union[str, FileExt])-> Union[str, None]:
    """[summary]

    Args:
        file_path (str): [description]
        ext (Union[str, FileExt]): [description]

    Returns:
        Union[str, None]: [description]
    """

    if not os.path.isfile(file_path):
        logger.error(f'File "{file_path}" does not exist or is not a file!')
        return None
    _, file_ext = os.path.splitext(file_path)
    if file_ext!= f'{ext}':
        logger.error(f'File "{file_path}"- is not a {ext}-file!')
        return None
    return file_path

################################################################################
# Save/Load pkl files
################################################################################
def save_as_pickle(file_path, class2save, verbose=False, append_ext=True):
    """
    """
    file_path= append_ext(file_path, FileExt.pkl) if append_ext else file_path
    with open(file_path, 'wb') as file:
        pickle.dump(class2save, file, pickle.HIGHEST_PROTOCOL)
    print_saving_verbose(file_path, class2save, verbose)

def load_pickle(file_path, class2upload=None):
    """[summary]

    Args:
        filename ([type]): [description]
        class2upload ([type], optional): [description]. Defaults to None.
        verbose (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """

    with open(file_path, 'rb') as file:
        loaded_class = pickle.load(file)
    # print_loading_verbose(filename, loaded_class, verbose)
    if not class2upload:
        return loaded_class
    set_existing_attrs(class2upload, loaded_class)
    return class2upload

def set_existing_attrs(class2upload, newclass):

    for key in newclass.__dict__.keys():
            if key in class2upload.__dict__.keys():
                setattr(class2upload,key, getattr(newclass,key))

    # for key in class2upload.__dict__.keys():
    #         setattr(class2upload, key, getattr(newclass,key))

################################################################################
# Save/Load txt files
################################################################################
def save_as_txt(file_path, class2save, verbose=True, append_ext=True):
    """[summary]

    Args:
        filename ([type]): [description]
        class2save ([type]): [description]
        verbose (bool, optional): [description]. Defaults to True.
        add_ext (bool, optional): [description]. Defaults to True.
    """
    file_path= append_ext(file_path, FileExt.txt) if append_ext else file_path
    
    list_of_strings = []
    if isinstance(class2save,str):
        list_of_strings.append(class2save)
    elif isinstance(class2save, list):
        for item in class2save:
            list_of_strings.append(f'{item}')
    elif isinstance(class2save, dict):
        list_of_strings.append('Dictionary form:')
        list_of_strings.append(json.dumps(class2save))
        list_of_strings.append('\n\nSingle attributes:')
        list_of_strings.extend([f'{key} = {class2save[key]},' for key in class2save ])      
    else:
        tmp_dict= class2save.__dict__
        list_of_strings.append('Dictionary form:')
        list_of_strings.append(json.dumps(class2save.__dict__))
        list_of_strings.append('\n\nSingle attributes:')
        single_attrs= [f'{key} = {tmp_dict[key]}' for key in class2save.__dict__ ]
        single_attrs= [ attr if len(attr)< 200 else f'{attr[:200]}...' for attr in single_attrs]
        list_of_strings.extend(single_attrs)

    with open(file_path, 'w') as file:
        [ file.write(f'{st}\n') for st in list_of_strings ]

    # print_saving_verbose(filepath, class2save, verbose)
def read_txt(file_path:str)-> Any:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if 'Dictionary form:' in lines[0]:
        return json.loads(lines[1].replace('\n', ''))

################################################################################
# Save/Load mat files
################################################################################
def save_as_mat(file_path:str, data:dict, append_ext:bool=True):
    from scipy.io.matlab.mio import savemat
    if not isinstance(data, dict):
        logger.error(f'Saving of {data=} in mat file - failed, data should be a dict')
        return
    savemat(file_path,data, appendmat=append_ext)

def load_mat(file_path:str)-> dict:
    from scipy.io.matlab.mio import loadmat
    if not verify_file(file_path, FileExt.mat):
        return
    file = loadmat(file_path)
    var = {key: file[key] for key in file.keys() if ("__") not in key}
    logger.debug(f'Loaded keys: {var.keys()} from file {os.path.split(file_path)[1]}')
    return var

      
# def load_file(file_path:str='', ext:Union[str, FileExt]=FileExt.mat, **kwargs):
#     """load all variables contained in a mat file in a dictionnary,
#     return the dict and the file_path (in case of selection by user)"""
#     _ , file_path= get_file_dir_path(file_path, ext=ext, **kwargs)
    
#     return var, file_path


################################################################################
# Methods
################################################################################
def append_ext(file_path:str, ext:Union[str, FileExt])->str:
    """ Append and or replace ext to the file path
    
    Args:
        filepath (str): path of the file
        ext (Union[str, FileExt]): ext 

    Returns:
        str: path of the file with ext
    """    
    return f'{os.path.splitext(file_path)[0]}{ext}'


def print_saving_verbose(filename, class2save= None, verbose=True):
    """[summary]

    Args:
        filename ([type]): [description]
        class2save ([type], optional): [description]. Defaults to None.
        verbose (bool, optional): [description]. Defaults to True.
    """

    if verbose:
        if hasattr(class2save, 'type'):
            print('\n{} saved in : ...{}'.format(class2save.type, filename[-50:]))
        else:
            print('\n Some data were saved in : ...{}'.format(filename[-50:]))
def print_loading_verbose(filename, classloaded= None, verbose=True):
    """[summary]

    Args:
        filename ([type]): [description]
        classloaded ([type], optional): [description]. Defaults to None.
        verbose (bool, optional): [description]. Defaults to True.
    """
    if verbose:
        if hasattr(classloaded, 'type'):
            print('\n{} object loaded from : ...{}'.format(classloaded.type, filename[-50:]))
        else:
            print('\nSome data were loaded from : ...{}'.format(filename[-50:]))

if __name__ == "__main__":
    from glob_utils.log.log  import main_log
    main_log()
    f=f'f {FileExt.txt}'
    print(f,  FileExt.mat )