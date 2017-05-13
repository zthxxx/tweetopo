# -*- coding: utf-8 -*-
import logging
import queue
from threading import Thread
from twitter.tweeapi import Twitter
import logsetting
from conffor import conffor
from database import mongo_orm as database
store = database.people_save
query = database.people_find

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
database.set_connect(**config["mongo"])
founds = set(database.get_uids())
seed_name = config['seed_name']
tokens = config["twitter"]

def store_user(twitter, uid=None, name=None):
    twitter.get_user(user_id=uid, screen_name=name).store_user(store)

def get_seed_people(seed_name):
    people = query(name=seed_name)
    if not people:
        store_user(Twitter(**tokens[0]), name=seed_name)
        people = query(name=seed_name)
    return people

def get_unfound_queue(friends, founds):
    unfound_set = set(friends) - set(founds)
    unfounds = queue.Queue()
    for uid in unfound_set:
        unfounds.put(uid)
    return unfounds

def query_from_queue(twitter, unfounds):
    while not unfounds.empty():
        uid = unfounds.get_nowait()
        store_user(twitter, uid=uid)
    logging.info('Task complete!')

def start_travers_crawling(tokens, unfounds):
    for token in tokens:
        twitter = Twitter(**token)
        task = Thread(target=query_from_queue, args=(twitter, unfounds))
        task.start()
    logging.info('Tasks started!')

if __name__ == "__main__":
    people = get_seed_people(seed_name)
    unfounds = get_unfound_queue(people.friends, founds)
    start_travers_crawling(tokens, unfounds)
