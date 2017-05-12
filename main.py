# -*- coding: utf-8 -*-
import logging
from twitter.tweeapi import Twitter
import logsetting
from conffor import conffor
from database import mongo_orm as database
store = database.people_save
query = database.people_find

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
database.set_connect(**config["mongo"])
twitter = Twitter(**config["twitter"])

seed_name = config['seed_name']

def store_user(uid=None, name=None):
    twitter.get_user(user_id=uid, screen_name=name).store_user(store)

def query_from_seed(seed_name):
    people = query(name=seed_name)
    founds = database.get_uids()
    if not people:
        store_user(name=seed_name)
        people = query(name=seed_name)
    for index, uid in enumerate(people.friends):
        if uid not in founds:
            logging.info([index, uid])
            store_user(uid=uid)
            founds.add(uid)

if __name__ == "__main__":
    query_from_seed(seed_name)
