# -*- coding: utf-8 -*-
from lib.twitter.tweeapi import Twitter, multi_tweecrawl
from lib.utils import _config
from lib.utils.db import confirm_unfound_queue, db

relate_store = db.relation.people_save
relate_query = db.relation.people_find

seed_name = _config['seed_name']
tokens = _config['twitter']


def store_relation(twitter, uid=None):
    twitter.store_user_relation(relate_store)


def get_seed_people(seed_name):
    people = relate_query(name=seed_name)
    if not people:
        Twitter(**tokens[0]) \
            .get_user(name=seed_name) \
            .store_user_relation(relate_store)
        people = relate_query(name=seed_name)
    return people


def get_crawl_queue(seed_name):
    friends = []
    founds = db.relation.get_uids()
    if not isinstance(seed_name, list):
        seed_name = [seed_name]
    for seed in seed_name:
        people = get_seed_people(seed)
        friends.extend(people.friends)
    unfounds = confirm_unfound_queue(friends, founds)
    return unfounds


def start_crawling_relation(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_relation)


def run():
    unfounds = get_crawl_queue(seed_name)
    start_crawling_relation(tokens, unfounds)
