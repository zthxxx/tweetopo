# -*- coding: utf-8 -*-
import logging
from twitter.tweeapi import Twitter
from conffor import conffor
from database import mongo_orm as database
store = database.people_save

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
database.set_connect(**config["mongo"])
twitter = Twitter(**config["twitter"])

seed_name = config['seed_name']

def store_user(uid=None, name=None):
    twitter.get_user(user_id=uid, screen_name=name).store_user(store)


if __name__ == "__main__":
    query = database.people_find
    people = query(name=seed_name)
    if people:
        for index, uid in enumerate(people.friends):
            print(index, uid)
            if not query(uid=uid):
                store_user(uid=uid)
