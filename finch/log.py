import logging.config
import traceback
from functools import wraps

import yaml

with open('finch/conf/logging.yml', 'r') as f:
    dict_conf = yaml.load(f, Loader=yaml.FullLoader)
logging.config.dictConfig(dict_conf)


def smart_decorator(decorator):
    """
    Base decorator for all decorators.
    :param decorator: The decorator being decorated.
    :return:
    """
    def decorator_proxy(func=None, **kwargs):
        if func is not None:
            return decorator(func=func, **kwargs)

        def decorator_proxy(func):
            return decorator(func=func, **kwargs)
        return decorator_proxy
    return decorator_proxy


@smart_decorator
def log(func, text=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug('Call %s' % func.__name__)
            logging.info(text)
            return func(*args, **kwargs)
        except Exception:
            logging.error(traceback.format_exc())
    return wrapper
