# -*- coding: utf-8 -*-
import logging
import queue

from lib.twitter.tweeapi import Twitter, multi_tweecrawl
from lib.utils import _config

account_seed = _config['account_seed']
if isinstance(account_seed, list):
    account_seed = account_seed[0]
tokens = _config['twitter']

twitter = None
uids_queue = queue.Queue()
seed_user_uid = None


def twitter_oauth():
    global twitter
    twitter_conf = tokens[0]
    twitter = Twitter(**twitter_conf)


def setup_module():
    twitter_oauth()


def try_none_api_user(twitter):
    try:
        twitter.get_friends()
    except Exception as e:
        logging.info('None of api or user for get friends should be error.')
        logging.info(e)


def test_get_api():
    api = twitter.api
    twitter.api = None
    try_none_api_user(twitter)
    twitter.api = api
    try_none_api_user(twitter)
    twitter.get_user(account=account_seed)


def test_store_user_relation():
    pages_limit = 1
    page_include = 5000

    def store_simulate(uid, account, protect, friends_count, friends, **kwargs):
        # if callback, user must not protected.
        assert not protect
        assert account == account_seed
        assert isinstance(uid, int)
        assert len(friends) == min(pages_limit * page_include, friends_count)

    twitter.store_user_relation(store=store_simulate, pages_limit=pages_limit)


def test_store_user_details():
    def store_simulate(
        uid, account, username, description, friends_count, followers_count,
        statuses_count, protect, verified, **kwargs
    ):
        global seed_user_uid
        assert account == account_seed
        assert isinstance(uid, int)
        seed_user_uid = uid
        uids_queue.put(uid)
        assert isinstance(username, str)
        assert isinstance(description, str)
        assert isinstance(friends_count, int)
        assert isinstance(followers_count, int)
        assert isinstance(statuses_count, int)
        assert isinstance(protect, bool)
        assert isinstance(verified, bool)

    twitter.store_user_details(store=store_simulate)


def test_multi_tweecrawl():
    # need seed_user_uid and uids_queue inited.
    def crawl_callback(twitter, uid):
        assert twitter.api is not None
        assert twitter.user is not None
        assert uid == seed_user_uid

    multi_tweecrawl(tokens, uids_queue, callback=crawl_callback)


def get_user(uid=None, account=None):
    user = None

    def set_user(result):
        nonlocal user
        user = result

    twitter.get_user(uid, account, set_user)
    return user


if __name__ == '__main__':
    setup_module()
    test_get_api()
    test_store_user_relation()
    test_store_user_details()
    test_multi_tweecrawl()
