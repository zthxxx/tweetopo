# -*- coding: utf-8 -*-
from mongoengine import *


def set_connect(host, port, database, user=None, passwd=None):
    return connect(db=database, host=host, port=port, username=user, password=passwd)
