import asyncio
import sys
from abc import ABCMeta, abstractmethod

import motor.motor_asyncio

from .decorators import *
from .validator import *


class FactoryInterface(metaclass=ABCMeta):
    """
    The interface of all runner factories
    """
    @abstractmethod
    def build_runner(self):
        """
        Build the runner
        """
        pass


class RunnerInterface(metaclass=ABCMeta):
    """
    The interface of all runners
    """
    @abstractmethod
    def run(self, test):
        """
        Run the runner
        """
        pass


class MongoRunner(RunnerInterface):
    """
    MongoDB runner base class
    """
    def __init__(self, mongo):
        self.mongo = mongo

    @retry()
    def query(self, test=None, result=None, client=None):
        pass

    def run(self, tests):
        result = {}
        client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://%s:%s@%s:%s/?authSource=%s' %
                                                        (self.mongo['username'], self.mongo['password'],
                                                         self.mongo['host'], self.mongo['port'], self.mongo['db']))
        tasks = [self.query(test=test, result=result, client=client) for test in tests]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        return result


class BondSolutionMongoRunner(MongoRunner):
    """
    Bond Solution MongoDB runner class
    """
    # @find()
    @count()
    def query(self, test=None, result=None, client=None):
        pass


class RunnerFactory(FactoryInterface):
    """
    Return specific runner.
    """
    def build_runner(*args, **kwargs):
        try:
            return globals()[args[0]](*args[1:], **kwargs)
        except Exception as e:
            logging.error('Invalid runner type: %s' % str(e))
            sys.exit(1)
