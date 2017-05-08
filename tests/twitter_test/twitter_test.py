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

def get_api_test():
    twitter.get_user(screen_name=seed_name)
