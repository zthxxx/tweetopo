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
    twitter_conf = config["twitter"][0]
    if 'proxy' in twitter_conf:
        del twitter_conf['proxy']
    twitter = Twitter(**twitter_conf)

def setup_module():
    twitter_oauth()

def get_api_test():
    twitter.get_user(screen_name=seed_name)

def store_user_simulate_test():
    pages_limit = 1
    page_include = 5000
    def store_simulate(name, uid, protect, friends_count, friends):
        # if callback, user must not protected.
        assert not protect
        assert name == seed_name
        assert isinstance(uid, int)
        assert len(friends) == min(pages_limit*page_include, friends_count)
    twitter.store_user(store=store_simulate, pages_limit=pages_limit)

if __name__ == '__main__':
    setup_module()
    get_api_test()
    store_user_simulate_test()
