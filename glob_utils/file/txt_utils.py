import json
import logging
from typing import Any
import glob_utils.file.utils

logger = logging.getLogger(__name__)


################################################################################
# Save/Load txt files with json data
################################################################################
def save_as_txt(file_path:str, obj:Any) -> None:
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
    file_path= glob_utils.file.utils.append_extension(file_path, glob_utils.file.utils.FileExt.txt)
    lines = []
    if isinstance(obj,str):
        lines.append(obj)
    elif isinstance(obj, list):
        lines.extend(f'{item}' for item in obj)
    elif isinstance(obj, dict):
        lines.extend(('Dictionary form:', json.dumps(obj), '\n\nSingle attributes:'))
        lines.extend([f'{key} = {obj[key]},' for key in obj ])
    else:
        tmp_dict= obj.__dict__
        lines.extend(
            (
                'Dictionary form:',
                json.dumps(obj.__dict__),
                '\n\nSingle attributes:',
            )
        )

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
    glob_utils.file.utils.is_file_with_ext(file_path, glob_utils.file.utils.FileExt.txt)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    logger.debug(f'{lines=}')
    if not lines:
        return None
    if 'Dictionary form:' in lines[0]:
        out= json.loads(lines[1].replace('\n', ''))
        glob_utils.file.utils.logging_file_loaded(file_path)
        return out
    