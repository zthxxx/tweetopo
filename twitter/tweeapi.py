# -*- coding: utf-8 -*-
import logging
import tweepy

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

    def get_user(self, user_id=None, screen_name=None):
        if not self._api:
            raise tweepy.TweepError('Api NOT inited!')
        user = self._api.get_user(user_id=user_id, screen_name=screen_name)
        self._user = user
        return self

    def authentication(method):
        def judge(self, *args, **kargs):
            if not self._api:
                raise tweepy.TweepError('Api NOT inited!')
            if not self._user:
                raise tweepy.TweepError('User NOT inited!')
            method(self, *args, **kargs)
            return self
        return judge

    @authentication
    def get_friends(self, callback=None, limit=0):
        api = self._api
        user = self._user
        cursor = tweepy.Cursor(api.friends, user_id=user.id, screen_name=user.screen_name)
        try:
            for index, friend in enumerate(cursor.items(limit)):
                if callable(callback):
                    callback(index, friend)
        except tweepy.TweepError as e:
            logging.warning([user.id, user.screen_name, e])

    @authentication
    def store_user(self, store=None, limit=0):
        user = self._user
        people = {
            "name": user.screen_name,
            "uid": user.id,
            "friends_count": user.friends_count,
            "friends": set()
        }
        self.get_friends(lambda i, friend: people["friends"].add(friend.id), limit)
        if callable(store):
            store(**people)






