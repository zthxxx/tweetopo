# -*- coding: utf-8 -*-
import logging

from mongoengine import *

from lib.conffor import conffor

PERSON_FIELD = ['uid', 'account', 'username', 'description', 'avatar', 'url', 'sign_at', 'location', 'time_zone',
                'friends_count', 'followers_count', 'statuses_count', 'favourites_count', 'protect', 'verified']


class Person(Document):
    """
    object field ref: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    """
    uid = IntField(required=True, primary_key=True)
    account = StringField()
    username = StringField()
    description = StringField()
    avatar = StringField()
    url = StringField()
    sign_at = DateTimeField()
    location = StringField()
    time_zone = StringField()
    friends_count = IntField()
    followers_count = IntField()
    statuses_count = IntField()
    favourites_count = IntField()
    protect = BooleanField()
    verified = BooleanField()
    meta = {
        'indexes': ['#uid']
    }


def people_save(uid, account, **kwargs):
    people = Person(uid=uid, account=account, **kwargs)
    try:
        people.save()
    except NotUniqueError:
        logging.warning([people.uid, people.account, 'has exist person collection..'])


def people_find(account='', uid=None):
    if uid is not None:
        people = Person.objects(uid=uid).first()
    else:
        people = Person.objects(account=account).first()
    return people


def get_uids():
    person = Person._get_collection()
    uidcour = person.find({}, {'_id': 1})
    uids = {people.get('_id') for people in uidcour}
    return uids


def export_persons(filename, uids=None, limit=0):
    columns = PERSON_FIELD
    person = Person._get_collection()
    query_obj = {}
    if uids:
        query_obj['_id'] = {'$in': uids}
    cour = person.find(query_obj).limit(limit)
    persons = {
        people.get('_id'): {
            column: people.get(column) for column in columns
        } for people in cour
    }
    for people in persons.values():
        if 'sign_at' in people:
            people['sign_at'] = str(people['sign_at'])
    conffor.dump(filename, persons, None)
    logging.info('Export all person info complete.')
