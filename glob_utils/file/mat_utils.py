

import logging
import re
from typing import Any

import glob_utils.file.utils
import glob_utils.types.dict
import numpy as np
import scipy.io.matlab.mio
import scipy.sparse

logger = logging.getLogger(__name__)

################################################################################
# Save/Load mat files
################################################################################
def save_as_mat(file_path:str, data:dict)->None:
    """Save data in a mat-file

    Args:
        file_path (str): saving path
        data (dict): dictionary to save
    """
    file_path= glob_utils.file.utils.append_extension(file_path, glob_utils.file.utils.FileExt.mat)
    if not isinstance(data, dict):
        logger.error(f'Saving of {data=} in mat file - failed, data should be a dict')
        return
    scipy.io.matlab.mio.savemat(file_path,data)
    glob_utils.file.utils.logging_file_saved(file_path)

def load_mat(file_path:str, logging:bool= True) -> dict:
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

    if not glob_utils.file.utils.check_file(file_path, glob_utils.file.utils.FileExt.mat):
        return None
    file = scipy.io.matlab.mio.loadmat(file_path,squeeze_me=True)

    var = {key: file[key] for key in file.keys() if "__" not in key[:2]}
    glob_utils.file.utils.logging_file_loaded(file_path)
    if logging:
        logger.debug(f'Loaded keys:{list(var.keys())}')
        
    return var


class MatFileStruct(object):
    
    separator:str='__'

    def __init__(self, separator:str='__') -> None:
        self.separator=separator
    
    def _extract_matfile(self, var_dict:dict, verbose:bool=False) -> dict:
        """
        """
        
        for key, val in var_dict.items():
            if verbose:
                logger.debug(f'{key}')
                logger.debug(f'type={type(val)} ')
            v= convert2python(val)
            var_dict[key]= v
            if verbose:
                logger.debug(f'type={type(v)} {v=}')

        struct=self.rebuild_matlab_struct(var_dict)
        struct=self.gather_top_key(struct)

        if verbose:
            glob_utils.types.dict.visualise(struct)

        return struct

    def gather_top_key(self, struct:dict) -> dict:

        new_struct= struct
        if 'type' not in struct or not struct['type']:
            return new_struct

        top_var = {key: val for key, val in struct.items() if not isinstance(val, dict)}
        
        for k in top_var:
            struct.pop(k)

        new_struct[top_var['type']]= top_var

        return new_struct

    def split_key(self, key:str, separator:str='__' )->tuple[str, str]:
        """Split the given key in a top- and a sub-part separated by the separator

            e.g. split_key('top__sub_part__2')
            >> ('top', 'sub_part__2')

        Args:
            key (str): _description_
            separator (str): Separator .Default is '__'

        Returns:
            tuple[str, str]: top- and a sub-part
        """
        idx=key.find(separator)
        top_key = key[:idx] if idx>=0 else key
        sub_key = key[idx+len(self.separator):] if idx>=0 else ''
        return top_key, sub_key
    
    def rebuild_matlab_struct(self, var_dict:dict)-> dict:

        struct={}
        for key, val in var_dict.items():

            top_key, sub_key= self.split_key(key)
            top_key, index= isa_struct_array(top_key)

            if index is None: # the var is a dict
                toSave = {sub_key:val} if sub_key else val
                if top_key not in struct:# init of the 
                    struct[top_key] = {} if sub_key else None
                
                if sub_key:
                    struct[top_key].update(toSave)
                else:
                    struct[top_key]= toSave

            else: # the var is list

                toSave = {sub_key:val} if sub_key else {'value':val}
                if top_key not in struct:# init of the 
                    struct[top_key] = {}
                
                if index not in struct[top_key]:# init of the 
                    struct[top_key].update({index:toSave})
                else:
                    struct[top_key][index].update(toSave)

        for key, val in struct.items():
            if isinstance(val, dict):
                struct[key]= self.rebuild_matlab_struct(val)
        
        return struct


def isa_struct_array(key:str, length_digit:int=3, separator:str='_')-> tuple[str, str]:
    """Check if a variable key correspond to a struct array

    In Matlab the data contained in the variable
    electrode = 1x3 struct array
                    {'nodes'}
                    {'zcontact'}
                    ....
    is saved in the mat_file for python as 
     'electrode_000__nodes'
     'electrode_000__zcontact'
     ....

     'electrode_003__nodes'
     'electrode_003__zcontact'


    Args:
        key (str): key to check
        length_digit (int, optional): length of digit of the index. Defaults to 3.
        separator (str, optional): separator between index and variable name. Defaults to '_'.

    Returns:
        tuple[str, str]: var_key, index. index is None if the variable is not a struct array
    """

    # logger.debug(f'{key=}')
    s_to_match= key[-(length_digit+len(separator)):]
    match=re.match( f'{separator}'+ r"\d{0,9}",s_to_match)

    # if s_to_match.isdigit():
        # return int(s_to_match)

    if match is not None and max(match.span(0))==length_digit+len(separator):
        return key[:-(length_digit+len(separator))], key[-length_digit:]

    return key, None

def convert2python(val) -> Any:

    if isinstance(val, (str, int, float, dict, list)):
        return val

    if isinstance(val,scipy.sparse.csc_matrix):
        return val

    if isinstance(val, np.ndarray) and val.size==0:
        return None

    return val

def str_cellarray2str_list(str_cellarray):
    """ After using loadmat, the str cell array have a strange shape
        >>> here the loaded "strange" array is converted to an str list

    Args:
        str_cellarray ( ndarray): correponing to str cell array in matlab

    Returns:
        str list: 
    """
    str_array=str_cellarray
    if str_cellarray.ndim ==2: 
        tmp= str_cellarray[0,:]
        str_array= [ t[0] for t in tmp]
    elif str_cellarray.ndim ==1:
        tmp= str_cellarray[0]
        str_array= tmp  

    return str_array 


if __name__ == "__main__":
    import logging

    from glob_utils.log.log import change_level_logging, main_log
    main_log()
    change_level_logging(logging.DEBUG)

    a = {'test': [{1:2}]}
    print(a['test'], type(a['test']))
    a['test'].insert(1,{3:4})
    print(a)
    print(a['test'])




    a= []
    a.insert(0,1)
    a.insert(3,2)
    print(a)
    print('fwd_model__stimulation_015__stim_pattern'.find('__'))
    print('fwd_model__stimulation_015__stim_pattern'[:9])
    print(isa_struct_array('electrode_007'))

    # # load_mat_file()
    file_path='E:/Software_dev/Matlab_datasets/20220307_093210_Dataset_name/Dataset_name_infos2py.mat'
