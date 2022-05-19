################################################################################
# Save/Load txt files with json data
################################################################################
import json
from typing import Any, Union
from glob_utils.file.utils import FileExt, append_extension, is_file_with_ext, logging_file_loaded, logging_file_saved
from glob_utils.types.dict import visualise, dict_nested
import numpy as np
from logging import getLogger


logger = getLogger(__name__)


class DebugEncoder():
    def default(self, obj):
        # print(f"not changed {obj=}, {type(obj)=}")
        return obj

class NumpyArrayEncoder(DebugEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            # print(f"int:{obj=}, {type(obj)=}")
            return int(obj)
        elif isinstance(obj, np.floating):
            # print(f"float:{obj=}, {type(obj)=}")
            return float(obj)
        elif isinstance(obj, np.ndarray):
            # print(f"ndarray:{obj=}, {type(obj)=}")
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

class ListEncoder(NumpyArrayEncoder):
    def default(self, obj):
        if not isinstance(obj, list):
            return super(ListEncoder, self).default(obj)

        for i, o in enumerate(obj):
            obj[i]= self.default(o)
        return obj

class DictEncoder(ListEncoder):
    def default(self, obj):
        if not isinstance(obj, dict):
            return super(DictEncoder, self).default(obj)

        for key, val in obj.items():
            obj[key]= self.default(val)
        return obj



class ListDecoder(NumpyArrayEncoder):

    def default(self, obj):
        if not isinstance(obj, list):
            return super(ListEncoder, self).default(obj)

        for i, o in enumerate(obj):
            obj[i]= self.default(o)
        return obj

class DictDecoder():
    def default(self, obj):
        if not isinstance(obj, dict):
            return obj
        
        if all( key in obj for key in ["array_real", "array_imag"]):
            return np.array(obj["array_real"]) + 1j *np.array(obj["array_imag"])

        for key, val in obj.items():
            obj[key]= self.default(val)

        return obj


def save_to_json(file_path:str, obj:dict, header:str= None) -> None:
    """Save an object in a txt-file

    if obj 
        (str)  -> line[0] = obj
        (list) -> line[i] = obj[i] (item_i)
        (dict) -> line[0] ='Dictionary form:'
                  line[1] = json of the dict
                  line[5] = Single attributes:' # list attrs for better readbility
                  line[6:] = 'key= value'
        
    Args:
        file_path (str): saving path
        obj (Any): object to save
    """
    file_path= append_extension(file_path, FileExt.json)
    if not isinstance(obj, dict):
        return
    obj=DictEncoder().default(obj)
    # visualise(obj)
    header = f"//JSON data of: {header}" if header is not None else '//JSON data:'

    lines = list((header, json.dumps(obj), '\n\n//Single attributes:'))
    lines.extend([f'//{key} = {obj[key]},' for key in obj ])


    # single_attrs= [f'{key} = {tmp_dict[key]}' for key in obj.__dict__ ]
    # single_attrs= [ attr if len(attr)< 200 else f'{attr[:200]}...' for attr in single_attrs]
    # lines.extend(single_attrs)

    with open(file_path, 'w') as file:
        [ file.write(f'{line}\n') for line in lines ]
    logging_file_saved(file_path)




def read_json(file_path:str)-> Union[dict, None]:
    """Load a txt file with json data

    Args:

    Returns:
        Any: return dict of the json saved data if found. None otherwise
    """
    file_path= append_extension(file_path, FileExt.json)
    file_path =is_file_with_ext(file_path, FileExt.json)
    if file_path is None:
        return None

    with open(file_path, 'r') as file:
        lines = file.readlines()
    # logger.debug(f'{lines=}')
    if not lines:
        return None

    if 'JSON data' not in lines[0]:
        return None
    out= json.loads(lines[1].replace('\n', ''))
    logging_file_loaded(file_path)
    return out


if __name__ == "__main__":
    """"""