# -*- coding: utf-8 -*-
from lib.twitter.tweeapi import multi_tweecrawl
from lib.utils import _config
from lib.utils.db import confirm_unfound_queue, db
from lib.utils.field import get_hub_uids, get_secondouts_uids

detail_store = db.person.people_save

account_seed = _config['account_seed']
tokens = _config['twitter']


def store_people_details(twitter, uid=None):
    user = twitter.user
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
    detail_store(**people)


def start_crawling_people_details(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, resolve=store_people_details)


def crawl_detail_from_hub():
    hub_uids = get_hub_uids()
    secondout_uids = get_secondouts_uids()
    founds = db.person.get_uids()
    unfounds = confirm_unfound_queue(hub_uids | secondout_uids, founds)
    start_crawling_people_details(tokens, unfounds)


def run():
    crawl_detail_from_hub()
