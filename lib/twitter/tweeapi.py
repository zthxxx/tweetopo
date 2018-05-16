# -*- coding: utf-8 -*-
import logging
from threading import Thread
import time

from retrying import retry
import tweepy

_FRIENDS_COUNT_MAX_ = 10000


def authentication(method):
    def judge(self, *args, **kwargs):
        if not self.api:
            raise tweepy.TweepError('Twitter api NOT ready!')
        if not self.user:
            raise tweepy.TweepError('Twitter user NOT ready!')
        method(self, *args, **kwargs)
        return self

    return judge


class Twitter:
    _IGNORE_ERROR_CODES = {326, 50, 63}

    # 326 - this account is temporarily locked.
    # 50 - User not found.
    # 63 - User has been suspended.

    def __init__(self,
                 consumer_key, consumer_secret,
                 access_token, access_token_secret,
                 proxy=''
                 ):
        self.api = None
        self.user = None
        self.config = {
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'proxy': proxy
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
            proxy=config['proxy']
        )
        self.api = api
        return self

    @retry(wait_random_min=15 * 1000, wait_random_max=25 * 1000, stop_max_attempt_number=5)
    def get_user(self, uid=None, account=None, resolve=None, reject=None):
        if not self.api:
            raise tweepy.TweepError('Twitter api NOT ready!')
        try:
            user = self.api.get_user(user_id=uid, screen_name=account)
            self.user = user
            if callable(resolve):
                resolve(user)
        except tweepy.TweepError as e:
            logging.error('Uid ({0}) and account ({1}) has error: {2}'.format(uid, account, e))
            if callable(reject):
                reject(uid, account, e)
            if e.api_code in self._IGNORE_ERROR_CODES:
                return None
            raise e
        return self

    @authentication
    def get_friends(self, resolve=None, reject=None, pages_limit=0):
        api = self.api
        user = self.user
        if user.friends_count > _FRIENDS_COUNT_MAX_:
            logging.warning('The user [%d]-[%s] has too many [%d] friends!'
                            % (user.id, user.screen_name, user.friends_count))
            return
        cursor = tweepy.Cursor(api.friends_ids, user_id=user.id, screen_name=user.screen_name)
        friends = []
        try:
            for friends_page in cursor.pages(pages_limit):
                friends.extend(friends_page)
            if callable(resolve):
                resolve(friends)
        except tweepy.TweepError as e:
            logging.error([user.id, user.screen_name, e])
            if callable(reject):
                reject(user, e)

    @authentication
    def get_timeline(self, resolve=None, reject=None, pages_limit=0):
        api = self.api
        user = self.user
        cursor = tweepy.Cursor(api.user_timeline, user_id=user.id, screen_name=user.screen_name,
                               trim_user=True, exclude_replies=False)
        timeline = []
        try:
            for timeline_page in cursor.pages(pages_limit):
                timeline.extend(timeline_page)
            if callable(resolve):
                resolve(timeline)
        except tweepy.TweepError as e:
            logging.error([user.id, user.screen_name, e])
            if callable(reject):
                reject(user, e)

    @authentication
    def store_user_relation(self, store=None, pages_limit=0):
        if not callable(store):
            return
        user = self.user
        friends = []

        def set_friends(result):
            nonlocal friends
            friends = result

        self.get_friends(set_friends, None, pages_limit)
        people = {
            'uid': user.id,
            'account': user.screen_name,
            'username': user.name,
            'protect': user.protected,
            'friends_count': user.friends_count,
            'friends': friends
        }
        store(**people)

    @authentication
    def store_user_details(self, store=None):
        if not callable(store):
            return
        user = self.user
        people = {
            'uid': user.id,
            'account': user.screen_name,
            'username': user.name,
            'description': user.description,
            'avatar': user.profile_image_url_https,
            'url': user.url,
            'sign_at': user.created_at,
            'location': user.location,
            'time_zone': user.time_zone,
            'friends_count': user.friends_count,
            'followers_count': user.followers_count,
            'statuses_count': user.statuses_count,
            'favourites_count': user.favourites_count,
            'protect': user.protected,
            'verified': user.verified
        }
        store(**people)


def multi_tweecrawl(tokens, uids_queue, block=True, **kwargs):
    """
    multi-threading for crawl twitter api with users id
    :param tokens: some twitter api tokens
    :param uids_queue: Queue of user ids
    :param block: is block for crawling
    :param kwargs: kwargs of thead (resolve)
    :return:
    """

    def thread_from_queue(index, twitter, resolve=None, reject=None):
        """
        :param index: thread index to start and sleep
        :param twitter: authentic instance of Twitter
        :param resolve: func of operate which receive two param (twitter, uid)
        :param reject: func of error operate which receive two param (twitter, uid)
        """
        if not callable(resolve):
            raise tweepy.TweepError('resolve is need in twitter crawl callback!')
        time.sleep(index)
        logging.info('Twitter thead-%d : tasks started!' % index)
        while not uids_queue.empty():
            uid = uids_queue.get_nowait()
            if twitter.get_user(uid=uid) is None:
                if callable(reject):
                    reject(twitter, uid=uid)
                continue
            resolve(twitter, uid=uid)
        logging.info('Twitter thead-%d : task complete!' % index)

    tasks = []
    for index, token in enumerate(tokens):
        if uids_queue.empty() or uids_queue.qsize() < index + 1:
            break
        twitter = Twitter(**token)
        task = Thread(name='Theading-%d' % (index + 1), target=thread_from_queue, args=(index + 1, twitter),
                      kwargs=kwargs)
        tasks.append(task)
        task.start()
    logging.info('Twitter tasks all started!')
    if block:
        for task in tasks:
            task.join()
        logging.info('Twitter tasks all complete!')
