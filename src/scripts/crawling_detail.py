# -*- coding: utf-8 -*-
from lib.twitter.tweeapi import multi_tweecrawl
from lib.utils import _config
from lib.utils.db import db, confirm_unfound_queue
from lib.utils.field import get_hub_uids, get_secondouts_uids

detail_store = db.person.people_save

seed_name = _config['seed_name']
tokens = _config["twitter"]


def store_people_details(twitter, uid=None):
    twitter.store_user_details(detail_store)


def start_crawling_people_details(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, callback=store_people_details)


def crawl_detail_from_hub():
    hub_uids = get_hub_uids()
    secondout_uids = get_secondouts_uids()
    founds = db.person.get_uids()
    unfounds = confirm_unfound_queue(hub_uids | secondout_uids, founds)
    start_crawling_people_details(tokens, unfounds)


def run():
    crawl_detail_from_hub()
