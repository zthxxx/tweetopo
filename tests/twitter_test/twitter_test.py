# -*- coding: utf-8 -*-
import logging
import queue
from conffor import conffor
from twitter.tweeapi import Twitter
from twitter.tweeapi import multi_tweecrawl

conf_file = './tweetconf.json'
config = conffor.load(conf_file)
seed_name = config['seed_name']
if isinstance(seed_name, list):
    seed_name = seed_name[0]
tokens = config["twitter"]

twitter = None
uids_queue = queue.Queue()
seed_user_uid = None

def tokens_filter():
    for token in tokens:
        if 'proxy' in token:
            del token['proxy']

def twitter_oauth():
    global twitter
    twitter_conf = tokens[0]
    twitter = Twitter(**twitter_conf)

def setup_module():
    tokens_filter()
    twitter_oauth()

def try_none_api_user(twitter):
    try:
        twitter.get_friends(None)
    except Exception as e:
        logging.info('None of api or user for get friends should be error.')
        logging.info(e)

def get_api_test():
    api = twitter._api
    twitter._api = None
    try_none_api_user(twitter)
    twitter._api = api
    try_none_api_user(twitter)
    twitter.get_user(name=seed_name)

def store_user_relation_test():
    pages_limit = 1
    page_include = 5000
    def store_simulate(name, uid, protect, friends_count, friends):
        # if callback, user must not protected.
        assert not protect
        assert name == seed_name
        assert isinstance(uid, int)
        assert len(friends) == min(pages_limit*page_include, friends_count)
    twitter.store_user_relation(store=store_simulate, pages_limit=pages_limit)

def store_user_details_test():
    def store_simulate(
        uid, name, fullname, description, sign_at, location,
        time_zone, friends_count, followers_count,
        statuses_count, url, protect, verified
    ):
        global seed_user_uid
        assert name == seed_name
        assert isinstance(uid, int)
        seed_user_uid = uid
        uids_queue.put(uid)
        assert isinstance(fullname, str)
        assert isinstance(description, str)
        assert isinstance(friends_count, int)
        assert isinstance(followers_count, int)
        assert isinstance(statuses_count, int)
        assert isinstance(protect, bool)
        assert isinstance(verified, bool)
    twitter.store_user_details(store=store_simulate)

def multi_tweecrawl_test():
    # need seed_user_uid and uids_queue inited.
    def crawl_callback(twitter, uid):
        assert twitter._api is not None
        assert twitter._user is not None
        assert uid == seed_user_uid
    multi_tweecrawl(tokens, uids_queue, callback=crawl_callback)

if __name__ == '__main__':
    setup_module()
    get_api_test()
    store_user_relation_test()
    store_user_details_test()
    multi_tweecrawl_test()
