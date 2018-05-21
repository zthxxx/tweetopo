# -*- coding: utf-8 -*-
from collections import Iterable
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
    friends = ListField(IntField())
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
    cour = Relation.objects.only('uid')
    uids = {people.uid for people in cour}
    return uids


def export_relation(filename, account_seed=None, limit=None):
    query = {}
    if account_seed:
        if not isinstance(account_seed, Iterable):
            account_seed = [account_seed]
        uids = set(account_seed)
        cour = Relation.objects(account__in=account_seed).only('uid', 'friends')
        for people in cour:
            uids.update(people.friends)
        query['uid__in'] = uids
    cour = Relation.objects(**query).only('uid', 'friends').limit(limit)
    persons = {people.uid: people.friends for people in cour}
    conffor.dump(filename, persons, None)
    logging.info('Export Relation relationship complete.')
