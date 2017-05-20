# -*- coding: utf-8 -*-
import logging
import queue
import logsetting
from twitter.tweeapi import Twitter
from twitter.tweeapi import multi_tweecrawl
from conffor import conffor
import database as db
from analyse_topology import get_hub_uids, hub_users_csv

relate_store = db.relation.people_save
relate_query = db.relation.people_find
detail_store = db.person.people_save

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
db.set_connect(**config["mongo"])
seed_name = config['seed_name']
tokens = config["twitter"]

def store_relation(twitter, uid=None):
    twitter.store_user_relation(relate_store)

def store_people_details(twitter, uid=None):
    twitter.store_user_details(detail_store)

def get_seed_people(seed_name):
    people = relate_query(name=seed_name)
    if not people:
        Twitter(**tokens[0])\
            .get_user(name=seed_name)\
            .store_user_relation(relate_store)
        people = relate_query(name=seed_name)
    return people

def get_unfound_queue(friends, founds):
    unfound_set = set(friends) - set(founds)
    logging.info('Remaining amount of people is %d' % len(unfound_set))
    unfounds = queue.Queue()
    for uid in unfound_set:
        unfounds.put(uid)
    return unfounds

def get_crawl_queue(seed_name):
    friends = []
    founds = set(db.relation.get_uids())
    if not isinstance(seed_name, list):
        seed_name = [seed_name]
    for seed in seed_name:
        people = get_seed_people(seed)
        friends.extend(people.friends)
    unfounds = get_unfound_queue(friends, founds)
    return unfounds

def start_crawling_relation(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_relation)

def start_crawling_people_details(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_people_details)

def crawl_detail_from_hub():
    hub_uids = get_hub_uids()
    founds = db.person.get_uids()
    unfounds = get_unfound_queue(hub_uids, founds)
    start_crawling_people_details(tokens, unfounds)

def export_hub_persons(filename):
    hub_uids = get_hub_uids(hub_users_csv)
    db.person.export_persons(filename, uids=list(hub_uids))

if __name__ == "__main__":
    unfounds = get_crawl_queue(seed_name)
    start_crawling_relation(tokens, unfounds)
    db.relation.export_relation('twitter_relations.json', seed_name=seed_name)

    # crawl_detail_from_hub()

    # export_hub_persons('hub_persons.json')
