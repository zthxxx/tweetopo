# -*- coding: utf-8 -*-
import logging
from mongoengine import *
from lib.conffor import conffor

class Relation(Document):
    name = StringField()
    uid = IntField(required=True, primary_key=True)
    friends_count = IntField()
    friends = ListField()
    protect = BooleanField()
    meta = {
        "indexes": ["#uid"]
    }

def people_save(name, uid, protect, friends_count, friends):
    people = Relation(name=name, uid=uid, protect=protect, friends_count=friends_count, friends=friends)
    try:
        people.save()
    except NotUniqueError as e:
        logging.warning([people.uid, people.name, "has exist in relation collection."])

def people_find(name='', uid=None):
    if uid is not None:
        people = Relation.objects(uid=uid).first()
    else:
        people = Relation.objects(name=name).first()
    return people

def get_uids():
    person = Relation._get_collection()
    uidcour = person.find({}, {"_id": 1})
    uids = {people.get('_id') for people in uidcour}
    return uids

def export_relation(filename, seed_name=None, limit=0):
    persons = dict()
    person = Relation._get_collection()
    query_obj = {}
    if seed_name:
        uids = set()
        seed_uids = set()
        if not isinstance(seed_name, list):
            seed_name = [seed_name]
        for name in seed_name:
            people = people_find(name=name)
            seed_uids.add(people.uid)
            uids.update(people.friends)
        uids.difference_update(seed_uids)
        query_obj['_id'] = {'$in': list(uids)}
    cour = person.find(query_obj, {"_id": 1, "friends":1}).limit(limit)
    for people in cour:
        persons[people['_id']] = people["friends"]
    conffor.dump(filename, persons, None)
    logging.info('Export Relation relationship complete.')
