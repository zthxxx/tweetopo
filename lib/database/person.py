# -*- coding: utf-8 -*-
import logging

from mongoengine import *

from lib.conffor import conffor
from lib.database.mongo_operator import doc2dict

PERSON_FIELD = ['uid', 'account', 'username', 'description', 'avatar', 'url', 'sign_at', 'location', 'time_zone',
                'friends_count', 'followers_count', 'statuses_count', 'favourites_count', 'protect', 'verified']


class Person(Document):
    """
    object field ref: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    uid: alias of twitter user object id
    account: alias of twitter user object screen_name
    username: alias of twitter user object name
    """
    uid = IntField(required=True, primary_key=True)
    account = StringField()
    username = StringField()
    description = StringField()
    avatar = URLField()
    url = URLField()
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
    cour = Person.objects.only('uid')
    uids = {people.uid for people in cour}
    return uids


def export_persons(filename, uids=None, limit=None):
    query = {}
    if uids:
        query['uid__in'] = uids
    cour = Person.objects(**query).limit(limit)
    persons = {
        people.uid: {
            **doc2dict(people),
            'sign_at': str(people.sign_at)
        } for people in cour
    }
    conffor.dump(filename, persons, None)
    logging.info('Export all person info complete.')
