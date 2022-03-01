import functools
import logging.config
import os
import traceback
import yaml

path = os.path.join(os.path.dirname(__file__), 'conf/logging.yml')
with open(path, 'r') as f:
    dict_conf = yaml.load(f, Loader=yaml.FullLoader)
logging.config.dictConfig(dict_conf)


def smart_decorator(decorator):
    def decorator_proxy(func=None, **kwargs):
        if func is not None:
            return decorator(func=func, **kwargs)

        def decorator_proxy(func):
            return decorator(func=func, **kwargs)
        return decorator_proxy
    return decorator_proxy


@smart_decorator
def log(func, text=None):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug('Call: %s args: %s kwargs: %s' % (func.__name__, args, kwargs))
            if text:
                logging.info('%s: %s args: %s kwargs: %s' % (text, func.__name__, args, kwargs))
            result = func(*args, **kwargs)
            return result
        except Exception:
            logging.error('Error: %s args: %s kwargs: %s' % (func.__name__, args, kwargs))
            logging.error(traceback.format_exc())
    return wrapper
