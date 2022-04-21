



import logging
import pandas as pd
import numpy as np
import glob_utils.file.utils

logger = logging.getLogger(__name__)



################################################################################
# Save/Load csv files
################################################################################


def save_as_csv(file_path:str, data:dict)->None:
    """Save data in a csv-file

    Args:
        file_path (str): saving path
        data (dict): The values of dict should be ndarray or list. And it will be converted to 1-D array for saving 
        csv-file. The length of data should be the same.
    """
    if not isinstance(data, dict):
        logger.error(f'Saving of {data=} in csv file - failed, data should be a dict')
        return
    
    # convert list to 1-D nparray if values of dict is list or nested list
    for key, values in data.items():
        if isinstance(values, list):
            data[key]= np.hstack(values)
    
    # convert to 1-D array if dim not 1
    data = {k: v.flatten() for k,v in data.items()} 

    file_path= glob_utils.file.utils.append_extension(file_path, glob_utils.file.utils.FileExt.csv)

    df = pd.DataFrame.from_dict(data) 
    df.to_csv(file_path, index = False, header=True,)

def load_csv(file_path:str) -> dict:
    """Load a csv-file.

    All variables contained in a csv-file (except the private var) are  
    return in a dictionnary

    Args:
        file_path (str): path of csv to load

    Returns:
        dict: variables contained in the csv-file
    """    
    if not glob_utils.file.utils.check_file(file_path, glob_utils.file.utils.FileExt.csv):
        return None
    return pd.read_csv(file_path).to_dict('list')