import logging
from functools import wraps

from .utils import update_test_result


def count():
    """
    Rerun the case when failed.
    """
    def validate(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logging.debug('Checkpoint: count, test: %s' % kwargs['test'])
            client = kwargs['client']
            db = client.bondsolution
            n = await db.bond.count_documents({})
            result = 'pass' if n > 0 else 'fail'
            message = None if n > 0 else 'count: %d' % n
            update_test_result(kwargs['result'], kwargs['test'], 'count', result, message)
            return func(*args, **kwargs)
        return wrapper
    return validate


def find():
    """
    Rerun the case when failed.
    """
    def validate(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logging.debug('Checkpoint: find, test: %s' % kwargs['test'])
            client = kwargs['client']
            db = client.bondsolution
            n = await db.bond.count_documents({})
            result = 'pass' if n > 0 else 'fail'
            message = None if n > 0 else 'count: %d' % n
            update_test_result(kwargs['result'], kwargs['test'], 'find', result, message)
            return func(*args, **kwargs)
        return wrapper
    return validate
