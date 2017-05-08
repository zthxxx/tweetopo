# -*- coding: utf-8 -*-
import logging
from twitter.tweeapi import Twitter
from conffor import conffor
from database import mongo_orm as database


if __name__ == "__main__":
    conf_file = './tweetconf.json'
    config = conffor.load(conf_file)
    seed_name = config['seed_name']
    database.set_connect(**config["mongo"])
    twitter = Twitter(**config["twitter"])
    user = twitter.get_user(screen_name=seed_name)

    people = {
        "name": user.screen_name,
        "uid": user.id,
        "friends_count": user.friends_count,
        "friends": set()
    }

    twitter.get_friends(lambda i,friend: people["friends"].add(friend.id))
    database.people_save(**people)

















