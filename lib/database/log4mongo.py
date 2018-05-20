from datetime import datetime
import logging

from mongoengine import *


class LogRecord(Document):
    """
    show recent log in db:
    ﻿db.log_record.find({}).sort({_id: -1}).limit(200)
    """
    occur_at = DateTimeField()  # datetime.fromtimestamp(record.created)
    channel = StringField()  # alias `name` in logging.Formatter
    thread_name = StringField()
    filename = StringField()
    lineno = IntField()
    levelname = StringField()
    message = StringField()


class MongoHandler(logging.Handler):
    def emit(self, record):
        try:
            log_record = {
                'occur_at': datetime.fromtimestamp(record.created),
                'channel': record.name,
                'thread_name': record.threadName,
                'filename': record.filename,
                'lineno': record.lineno,
                'levelname': record.levelname,
                'message': record.getMessage()
            }
            LogRecord(**log_record).save()
        except MongoEngineConnectionError:
            remove_log4mongo()
        except Exception:
            self.handleError(record)


def remove_log4mongo():
    root = logging.getLogger()
    removed = filter(lambda handler: not isinstance(handler, MongoHandler), root.handlers)
    root.handlers = list(removed)


def add_log4mongo():
    remove_log4mongo()
    root = logging.getLogger()
    root.addHandler(MongoHandler())
