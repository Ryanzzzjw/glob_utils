

import logging
import traceback
import glob_utils.log.log

logger = logging.getLogger(__name__)

# decorator for catching error without making buuuing the app...
def catch_error(func):
    '''Decorator that reports the execution time.'''
  
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException as e:
            msg= f'in {func.__name__}: {e}\n {traceback.format_exc()}'
            if glob_utils.log.log.check_logger_exist():
                logger.error(msg)
            else:
                print(f'Error {msg}')

    return wrap
