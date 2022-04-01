import datetime
import json
import logging
import os

from mongoengine import *


class finch_result(Document):
    _id = StringField(required=True)
    env = StringField(required=True)
    job = StringField(required=True)
    pass_rate = FloatField(required=True)
    fail = IntField(required=True)
    total = IntField(required=True)
    duration = FloatField(required=True)
    execution_time = DateTimeField(default=datetime.datetime.utcnow())
    test = ListField()


def save_result(id, env, job, result_summary, duration, result):
    """
    Save result to db.
    """
    finch_result(_id=id, env=env, job=job, pass_rate=result_summary[0], fail=result_summary[1], total=result_summary[2],
                 duration=duration, test=result).save()
    logging.info('Data saved at finch_result')


def connect_db():
    """
    Connect to MongoDB.
    :return:
    """
    path = os.path.join(os.path.dirname(__file__), 'conf/env.json')
    with open(path) as json_file:
        data = json.load(json_file)
        db = data["mongo"]["db"]
        host = data["mongo"]["host"]
        port = data["mongo"]["port"]
        username = data["mongo"]["username"]
        password = data["mongo"]["password"]

    uri = 'mongodb://%s:%s@%s:%s' % (username, password, host, port)
    connect(db, host=uri)
