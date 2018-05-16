# -*- coding: utf-8 -*-
import logging

from mongoengine import *

from lib.conffor import conffor


class Relation(Document):
    """
    uid: alias of twitter user object id
    account: alias of twitter user object screen_name
    username: alias of twitter user object name
    """
    uid = IntField(required=True, primary_key=True)
    account = StringField()
    username = StringField()
    protect = BooleanField()
    friends_count = IntField()
    friends = ListField()
    meta = {
        'indexes': ['#uid']
    }


def people_save(uid, account, **kwargs):
    people = Relation(uid=uid, account=account, **kwargs)
    try:
        people.save()
    except NotUniqueError:
        logging.warning([people.uid, people.account, 'has exist in relation collection.'])


def people_find(account='', uid=None):
    if uid is not None:
        people = Relation.objects(uid=uid).first()
    else:
        people = Relation.objects(account=account).first()
    return people


def get_uids():
    person = Relation._get_collection()
    uidcour = person.find({}, {'_id': 1})
    uids = {people.get('_id') for people in uidcour}
    return uids


def export_relation(filename, account_seed=None, limit=0):
    persons = dict()
    person = Relation._get_collection()
    query_obj = {}
    if account_seed:
        uids = set()
        seed_uids = set()
        if not isinstance(account_seed, list):
            account_seed = [account_seed]
        for account in account_seed:
            people = people_find(account=account)
            seed_uids.add(people.uid)
            uids.update(people.friends)
        uids.difference_update(seed_uids)
        query_obj['_id'] = {'$in': list(uids)}
    cour = person.find(query_obj, {'_id': 1, 'friends': 1}).limit(limit)
    for people in cour:
        persons[people['_id']] = people['friends']
    conffor.dump(filename, persons, None)
    logging.info('Export Relation relationship complete.')
