# -*- coding: utf-8 -*-
from mongoengine import *
from mongoengine.base import BaseDocument


def set_connect(host, port, database, user=None, passwd=None):
    return connect(db=database, host=host, port=port, username=user, password=passwd)


def doc2dict(doc):
    if isinstance(doc, list):
        return [doc2dict(item) for item in doc]
    if isinstance(doc, BaseDocument):
        return {
            field: doc2dict(doc[field])
            for field in doc
            if doc[field] is not None
        }
    return doc
