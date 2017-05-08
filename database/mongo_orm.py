# -*- coding: utf-8 -*-
import logging
from mongoengine import *

def set_connect(host, port, database, user=None, passwd=None):
    return connect(db=database, host=host, port=port, username=user, password=passwd)

class Person(Document):
    name = StringField()
    uid = IntField(required=True, primary_key=True)
    friends_count = IntField()
    friends = ListField()
    meta = {
        "indexes": ["#uid"]
    }

def people_save(name, uid, friends_count, friends):
    people = Person(name=name, uid=uid, friends_count=friends_count, friends=friends)
    try:
        people.save()
    except NotUniqueError as e:
        logging.warning([people.uid, people.name, "has exist."])






