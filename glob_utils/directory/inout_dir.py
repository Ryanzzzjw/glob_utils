
from typing import Union
import glob_utils.file.utils
import glob_utils.file.txt_utils
from glob_utils.directory.utils import OpenDialogDirCancelledException, dir_exist, get_dir
from enum import Enum
import sys
from logging import getLogger
logger = getLogger(__name__)

################################################################################
# management of global default directory
################################################################################
class DirsList(Enum):
    input= 'input'
    output= 'output'


class DefaultDir_old(object):
    """Contain the default input- and output path of an application"""    
    _dirs: dict =None

    def __init__(self, input_dir:str='input', output_dir:str='output') -> None:
        self._dirs = {
            DirsList.input.value: input_dir,
            DirsList.output.value: output_dir
        }
        self.check_dirs()

    # @property
    # def input(self):
    #     return self._dirs['input']

    # @property
    # def output(self):
    #     return self._dirs['output']

    def default_dir(self, key:DirsList):
        return self._dirs[key.value]

    def set_dir(self, dir_path:str, dir_label:DirsList):
        self._dirs[dir_label.value]= dir_path
        self.check_dirs()

    def check_dirs(self):
        """ check if the input and output directoryies exist

        if not ask the user to select some via explorer dialog

        """
        for dir_label, dir_path in self._dirs.items():

            if not dir_exist(dir_path):
                new_dir=get_dir(
                            title=f'Select a default {dir_label} directory'
                )
                self._dirs[dir_label]=new_dir
                logger.info(f'Set "{dir_label}"-Directory to {new_dir}')
            else:
                logger.info(f'"{dir_label}"-Directory is : {new_dir}')
class DefaultDir(object):
    """Contain the default input- and output path of an application"""    
    _dirs: dict =None

    def __init__(self) -> None:
        self._dirs = {}

    def get(self, key:Union[str, Enum]=None)-> Union[str, dict]:
        if isinstance(key, Enum):
            key= key.value
        return self._dirs[key] if key else self._dirs

    def add_dir(self, dir_label:str, dir_path:str):
        self._dirs[dir_label]= dir_path
        self.check_dirs()

    def check_dirs(self):
        """ check if the input and output directoryies exist

        if not ask the user to select some via explorer dialog

        """
        _dirs={}
        for dir_label, dir_path in self._dirs.items():
            if not dir_exist(dir_path):
                try:
                    new_dir=get_dir(
                        title=f'Select a default "{dir_label}" directory'
                    )
                except OpenDialogDirCancelledException as e:
                    logger.critical(f'{e}')
                    sys.exit()
                _dirs[dir_label]=new_dir
            else:
                _dirs[dir_label]=dir_path
        self._dirs= _dirs

    def log_default_dir(self):

        l=[f'"{dir_label}": {dir_path}' for dir_label, dir_path in self._dirs.items()]
        list_2log= 'Default directories:\n'+'Directory : Path \n'+'\n'.join(l)
        logger.info(list_2log)

def set_default_dir(reset:bool, DIR:DefaultDir, init_dirs:dict, path:str) -> DefaultDir:

    logger.info('Setting default dirs: Start ...')
    dirs = None
    if glob_utils.file.utils.is_file_with_ext(path=path, ext=glob_utils.file.utils.FileExt.txt):
        dirs = None if reset else glob_utils.file.txt_utils.read_txt(path)

    dirs = dirs or init_dirs

    [DIR.add_dir(k, v) for k, v in dirs.items()]
    DIR.log_default_dir()
    glob_utils.file.txt_utils.save_as_txt(
        path,
        DIR.get())
    logger.info('Setting default dirs: Done')
    return DIR

if __name__ == "__main__":
    """"""
    # DEFAULT_DIRS= DefaultDir()   
    # print(DEFAULT_DIRS.input, DEFAULT_DIRS.output)
    # DEFAULT_DIRS.check_dirs()