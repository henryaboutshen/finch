import json
import logging
import os
import time

from functools import wraps


path = os.path.join(os.path.dirname(__file__), 'conf/config.json')
with open(path) as json_file:
    data = json.load(json_file)
    retries = data["retries"]


def retry():
    """
    Rerun the case when failed.
    """

    def try_rerun(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logging.debug('Retry decorator')
            if retries:
                for x in range(retries):
                    await func(*args, **kwargs)
                    results = [checkpoint['result'] for checkpoint in kwargs['result'][kwargs['test']]]
                    if 'fail' not in results:
                        logging.debug('Run[%s] pass!' % x)
                        break
                    else:
                        time.sleep(3 * x)
                        logging.debug('Run[%s]: fail!' % x)
            else:
                await func(*args, **kwargs)
        return wrapper
    return try_rerun
