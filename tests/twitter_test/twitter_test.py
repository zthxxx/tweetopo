# -*- coding: utf-8 -*-
import logging
from twitter.tweeapi import Twitter
from conffor import conffor

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
seed_name = config['seed_name']
twitter = None

def twitter_oauth():
    global twitter
    twitter_conf = config["twitter"]
    del twitter_conf['proxy']
    twitter = Twitter(**twitter_conf)

def setup_module():
    twitter_oauth()

def get_api_test():
    twitter.get_user(screen_name=seed_name)

def store_user_simulate_test():
    limit = 20
    def store_simulate(name, uid, friends_count, friends):
        assert name == seed_name
        assert isinstance(uid, int)
        assert len(friends) == min(limit, friends_count)
    twitter.store_user(store=store_simulate, limit=limit)
    
if __name__ == '__main__':
    setup_module()
    get_api_test()
    store_user_simulate_test()
