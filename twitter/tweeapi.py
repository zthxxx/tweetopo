# -*- coding: utf-8 -*-
import time
import logging
from threading import Thread
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

    @retry(wait_random_min=10*1000, wait_random_max=20*1000, stop_max_attempt_number=5)
    def get_user(self, uid=None, name=None):
        if not self._api:
            raise tweepy.TweepError('Api NOT inited!')
        try:
            user = self._api.get_user(user_id=uid, screen_name=name)
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
    def store_user_relation(self, store=None, pages_limit=0):
        user = self._user
        friends = []
        def set_friends(list):
            nonlocal friends
            friends = list
        if callable(store):
            self.get_friends(set_friends, pages_limit)
            people = {
                "name": user.screen_name,
                "uid": user.id,
                "protect": user.protected,
                "friends_count": user.friends_count
            }
            people["friends"] = friends
            store(**people)

    @authentication
    def store_user_details(self, store=None):
        user = self._user
        if callable(store):
            people = {
                'uid': user.id,
                'name': user.screen_name,
                'fullname': user.name,
                'description': user.description,
                'sign_at': user.created_at,
                'location': user.location,
                'time_zone': user.time_zone,
                'friends_count': user.friends_count,
                'followers_count': user.followers_count,
                'statuses_count': user.statuses_count,
                'url': user.url,
                'protect': user.protected,
                'verified': user.verified
            }
            store(**people)

def multi_tweecrawl(tokens, uids_queue, block=True, **kwargs):
    '''
    multi-threading for crawl twitter api with users id
    :param tokens:
    :param uids_queue:
    :param block:
    :param kwargs:
    :return:
    '''
    def thread_from_queue(index, twitter, callback=None):
        '''
        :param index: thread index to start and sleep
        :param twitter: authentic instance of Twitter
        :param callback: func of operate which receive two param (twitter, uid)
        '''
        time.sleep(index)
        logging.info('Twitter thead-%d : tasks started!' % index)
        if callable(callback):
            while not uids_queue.empty():
                uid = uids_queue.get_nowait()
                twitter.get_user(uid=uid)
                callback(twitter, uid=uid)
        logging.info('Twitter thead-%d : task complete!' % index)

    tasks = []
    for index, token in enumerate(tokens):
        twitter = Twitter(**token)
        task = Thread(target=thread_from_queue, args=(index+1, twitter), kwargs=kwargs)
        tasks.append(task)
        task.start()
    logging.info('Twitter tasks all started!')
    if block:
        for task in tasks:
            task.join()
        logging.info('Twitter tasks all complete!')
