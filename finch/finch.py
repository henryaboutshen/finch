import getopt
import logging.config
import os
import time
import sys
import json
import yaml

from . import model
from .runner import RunnerFactory
from .utils import get_test_result


def run_cli(argv):
    """
    Command line execution.
    """
    id = None
    env = None
    runner_type = None
    job = None
    tests = ['hanrui', 'xi']

    job_start_time = time.time()

    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "id=", "env=", "job="])
    except getopt.GetoptError:
        print('usage: python -m finch --id <multi-job-id> --env <environment> --job <job>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('usage: python -m finch --id <multi-job-id> --env <environment> --job <job>')
            sys.exit()
        elif opt == '--id':
            id = arg
        elif opt == '--env':
            env = arg
        elif opt == '--job':
            job = arg

    # Get config
    path = os.path.join(os.path.dirname(__file__), 'conf/config.json')
    with open(path) as json_file:
        data = json.load(json_file)
        save_db = data['save_db']
        for runner in data['runner']:
            for job_type in data['runner'][runner]:
                if job_type == job:
                    runner_type = runner
                    break
    if runner_type is None:
        logging.info("Illegal runner type!")
        sys.exit(1)

    path = os.path.join(os.path.dirname(__file__), 'conf/logging.yml')
    with open(path, 'r') as f:
        dict_conf = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(dict_conf)
    logging.info('Parameters: %s' % argv)

    path = os.path.join(os.path.dirname(__file__), 'conf/env.json')
    with open(path) as json_file:
        mongo = json.load(json_file)
    if mongo is None:
        logging.info("Illegal mongo environment!")
        sys.exit(1)

    # Execute test
    logging.info('Total tests: %s' % len(tests))
    runner = RunnerFactory.build_runner(runner_type, mongo[env])
    result = runner.run(tests)
    logging.debug('Result: %s' % result)
    fail_exist, result_summary = get_test_result(env, result)
    logging.info('Fail test exist: %s' % fail_exist)

    job_end_time = time.time()

    # Save result to database
    if save_db is True and result is not None:
        model.connect_db()
        model.save_result(id, env, job, result_summary, job_end_time - job_start_time, result)
    logging.info('Finch finished!')
    if fail_exist is True:
        sys.exit(1)
