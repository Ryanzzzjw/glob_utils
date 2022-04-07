

import logging
import traceback
from typing import Any, Union
import glob_utils.log.log

logger = logging.getLogger(__name__)

# decorator for catching error without making buuuing the app...
def catch_error(func):
    '''Decorator that catch all BaseException 
    and return it in log with traceback. it return the func result or
    `None` if an error occurs '''
  
    def wrap(*args, **kwargs)->Union[Any, None]:
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            msg= f'in {func.__name__}: {e}\n {traceback.format_exc()}'
            if glob_utils.log.log.check_logger_exist():
                logger.error(msg)
            else:
                print(f'Error {msg}')
            return None
    return wrap

if __name__ == "__main__":
    """"""