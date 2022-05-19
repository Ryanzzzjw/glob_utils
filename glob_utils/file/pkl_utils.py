
import logging
import os
import pickle
from typing import Any
import glob_utils.file.utils

logger = logging.getLogger(__name__)


################################################################################
# Save/Load pkl files
################################################################################
def save_as_pickle(file_path:str, obj:Any)->None:
    """Save an object in a pkl-file

    Args:
        file_path (str): saving path
        obj (Any): object to save
    """
    file_path= glob_utils.file.utils.append_extension(file_path, glob_utils.file.utils.FileExt.pkl)
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)
    glob_utils.file.utils.logging_file_saved(file_path)

def load_pickle(file_path:str, obj:Any=None)->Any:
    """Load an Object out of an pkl-file

    Args:
        file_path (str): pkl-file to load
        obj (Any, optional): Object to update. Defaults to None.

    Returns:
        Any: loaded object or the passed object with updated attributes
    """
    glob_utils.file.utils.is_file_with_ext(file_path, glob_utils.file.utils.FileExt.pkl)
    with open(file_path, 'rb') as file:
        loaded_obj = pickle.load(file)
    glob_utils.file.utils.logging_file_loaded(file_path)
    if not obj:
        return loaded_obj
    glob_utils.file.utils.set_existing_attrs(obj, loaded_obj)
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
        raise glob_utils.file.utils.EmptyFileError(f'{file_path} - File empty!')

    return load_pickle(file_path, obj)
