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


def test_user_get_friends():
    pages_limit = 1
    page_include = 5000

    def resolve_simulate(user, friends):
        # if callback, user must not protected.
        assert not user.protected
        assert user.screen_name == account_seed
        assert isinstance(user.id, int)
        assert len(friends) == min(pages_limit * page_include, user.friends_count)

    twitter.get_friends(resolve_simulate, pages_limit=pages_limit)


def test_user_field_type():
    user = twitter.user
    global seed_user_uid
    assert user.screen_name == account_seed
    assert isinstance(user.id, int)
    seed_user_uid = user.id
    uids_queue.put(user.id)
    assert isinstance(user.name, str)
    assert isinstance(user.description, str)
    assert isinstance(user.friends_count, int)
    assert isinstance(user.followers_count, int)
    assert isinstance(user.statuses_count, int)
    assert isinstance(user.protected, bool)
    assert isinstance(user.verified, bool)


def test_get_timeline():
    pages_limit = 1
    page_include = 200

    def resolve_simulate(statuses):
        assert len(statuses) == min(pages_limit * page_include, twitter.user.statuses_count)

    twitter.get_timeline(resolve_simulate, pages_limit=pages_limit)


def test_multi_tweecrawl():
    # need seed_user_uid and uids_queue inited.
    def crawl_callback(twitter, uid):
        assert twitter.api is not None
        assert twitter.user is not None
        assert uid == seed_user_uid

    multi_tweecrawl(tokens, uids_queue, callback=crawl_callback)


def access_verify():
    def log_invalid(auth, index):
        logging.error('#%d token invalid or expired, tips: \n' % index +
                      'consumer_key: %s \n' % auth.consumer_key +
                      'access_token: %s' % auth.access_token)

    token_count = len(tokens)
    accessed = 0
    for index, token in enumerate(tokens):
        api = Twitter(**token).api
        try:
            user = api.verify_credentials()
            if user:
                accessed += 1
                logging.warning('Succeed verify token %d/%d' % (accessed, token_count))
            else:
                log_invalid(api.auth, index)
        except Exception as e:
            log_invalid(api.auth, index)
            logging.error(e)
    logging.warning('Total succeed verify token %d/%d' % (accessed, token_count))


if __name__ == '__main__':
    # access_verify()
    setup_module()
    test_get_api()
    test_user_get_friends()
    test_user_field_type()
    test_get_timeline()
    test_multi_tweecrawl()
