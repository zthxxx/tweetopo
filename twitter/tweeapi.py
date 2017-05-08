# -*- coding: utf-8 -*-
import tweepy

class Twitter():
    def __init__(self,
        consumer_key, consumer_secret,
        access_token, access_token_secret,
        proxy=''
    ):
        self.api = None
        self.user = None
        self.config = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "proxy": proxy
        }
        self.get_tweeapi()

    def get_tweeapi(self):
        config = self.config
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
        self.api = api
        return api

    def get_user(self, user_id=None, screen_name=None):
        if not self.api:
            raise tweepy.TweepError('Api NOT inited!')
        user = self.api.get_user(user_id=user_id, screen_name=screen_name)
        self.user = user
        return self.user

    def get_friends(self, callback, limit=0):
        api = self.api
        user = self.user
        if not (api and user):
            raise tweepy.TweepError('Api or user NOT inited!')
        cursor = tweepy.Cursor(api.friends, user_id=user.id, screen_name=user.screen_name)
        for index, friend in enumerate(cursor.items(limit)):
            if callable(callback):
                callback(index, friend)






