# -*- coding: utf-8 -*-
import logging
from mongoengine import *
from conffor import conffor

def set_connect(host, port, database, user=None, passwd=None):
    return connect(db=database, host=host, port=port, username=user, password=passwd)

class Person(Document):
    name = StringField()
    uid = IntField(required=True, primary_key=True)
    friends_count = IntField()
    friends = ListField()
    protect = BooleanField()
    meta = {
        "indexes": ["#uid"]
    }

def people_save(name, uid, protect, friends_count, friends):
    people = Person(name=name, uid=uid, protect=protect, friends_count=friends_count, friends=friends)
    try:
        people.save()
    except NotUniqueError as e:
        logging.warning([people.uid, people.name, "has exist."])

def people_find(name='', uid=None):
    if uid is not None:
        people = Person.objects(uid=uid).first()
    else:
        people = Person.objects(name=name).first()
    return people

def get_uids():
    person = Person._get_collection()
    getid = lambda item: item.get('_id')
    uidcour = person.find({}, {"_id": 1})
    uids = set(map(getid,uidcour))
    return uids

def export_person(filename, limit=0):
    persons = dict()
    person = Person._get_collection()
    cour = person.find({}, {"_id": 1, "friends":1}).limit(limit)
    for people in cour:
        persons[people['_id']] = {"following": people["friends"], "followers": []}
    conffor.dump(filename, persons, None)
    logging.info('Export Person relationship complete.')
