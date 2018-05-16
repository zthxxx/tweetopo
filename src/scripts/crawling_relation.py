# -*- coding: utf-8 -*-
from lib.twitter.tweeapi import Twitter, multi_tweecrawl
from lib.utils import _config
from lib.utils.db import confirm_unfound_queue, db

relate_store = db.relation.people_save
relate_query = db.relation.people_find

account_seed = _config['account_seed']
tokens = _config['twitter']


def store_relation(twitter, uid=None):
    twitter.store_user_relation(relate_store)


def get_seed_people(account_seed):
    people = relate_query(account=account_seed)
    if not people:
        Twitter(**tokens[0]) \
            .get_user(account=account_seed) \
            .store_user_relation(relate_store)
        people = relate_query(account=account_seed)
    return people


def get_crawl_queue(account_seed):
    friends = []
    founds = db.relation.get_uids()
    if not isinstance(account_seed, list):
        account_seed = [account_seed]
    for account in account_seed:
        people = get_seed_people(account)
        friends.extend(people.friends)
    unfounds = confirm_unfound_queue(friends, founds)
    return unfounds


def start_crawling_relation(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, resolve=store_relation)


def run():
    unfounds = get_crawl_queue(account_seed)
    start_crawling_relation(tokens, unfounds)
