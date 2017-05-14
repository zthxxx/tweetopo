# -*- coding: utf-8 -*-
import logging
import tweepy
from retrying import retry

class Twitter():
    def __init__(self,
        consumer_key, consumer_secret,
        access_token, access_token_secret,
        proxy=''
    ):
        self._api = None
        self._user = None
        self._config = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "proxy": proxy
        }
        self.get_tweeapi()

    def get_tweeapi(self):
        config = self._config
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])
        api = tweepy.API(
            auth_handler=auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True,
            timeout=300,
            compression=True,
            proxy=config.get('proxy', '')
        )
        self._api = api
        return self

    @retry(wait_random_min=10*1000, wait_random_max=20*1000, stop_max_attempt_number=20)
    def get_user(self, user_id=None, screen_name=None):
        if not self._api:
            raise tweepy.TweepError('Api NOT inited!')
        try:
            user = self._api.get_user(user_id=user_id, screen_name=screen_name)
        except tweepy.TweepError as e:
            logging.error(e)
            raise e
        self._user = user
        return self

    def authentication(method):
        def judge(self, *args, **kwargs):
            if not self._api:
                raise tweepy.TweepError('Api NOT inited!')
            if not self._user:
                raise tweepy.TweepError('User NOT inited!')
            method(self, *args, **kwargs)
            return self
        return judge

    @authentication
    def get_friends(self, callback, pages_limit=0):
        api = self._api
        user = self._user
        cursor = tweepy.Cursor(api.friends_ids, user_id=user.id, screen_name=user.screen_name)
        friends = []
        try:
            for friends_page in cursor.pages(pages_limit):
                friends.extend(friends_page)
            if callable(callback):
                callback(friends)
        except tweepy.TweepError as e:
            logging.warning([user.id, user.screen_name, e])

    @authentication
    def store_user(self, store=None, pages_limit=0):
        user = self._user
        friends = []
        def set_friends(list):
            nonlocal friends
            friends = list
        self.get_friends(set_friends, pages_limit)
        people = {
            "name": user.screen_name,
            "uid": user.id,
            "protect": user.protected,
            "friends_count": user.friends_count
        }
        people["friends"] = friends
        if callable(store):
            store(**people)

