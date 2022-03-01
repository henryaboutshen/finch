import json
import logging
import os
import time

from functools import wraps

from .utils import get_keys

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
        def wrapper(*args, **kwargs):
            if retries:
                try:
                    rerun_time = get_keys(args[0].env, kwargs['test'], 'rerun_time')[0]
                except Exception as e:
                    logging.info('No rerun info for this case' + str(e))
                for x in range(retries):
                    func(*args, **kwargs)
                    comments = json.dumps(kwargs['test']['result']['comments'])
                    if 'fail' not in comments:
                        logging.info('Run[%s] pass!' % x)
                        break
                    else:
                        time.sleep(3 * x)
                        logging.info('Run[%s]: fail - %s' % (x, comments))
                        if x != retries - 1:
                            kwargs['test']['result'] = {'comments': {}}
            else:
                func(*args, **kwargs)
        return wrapper
    return try_rerun
