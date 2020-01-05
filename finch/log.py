import logging.config
import traceback
from functools import wraps

import yaml

with open('logging.yml', 'r') as f:
    dict_conf = yaml.load(f, Loader=yaml.FullLoader)
logging.config.dictConfig(dict_conf)

# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warn message')
# logging.error('error message')
# logging.critical('critical message')


def exception(func):
    @wraps(func)
    def log(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.error(traceback.format_exc())
    return log


@exception
def start():
    1 / 0


start()
