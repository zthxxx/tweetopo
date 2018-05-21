from lib.twitter.tweeapi import Twitter, multi_tweecrawl
from lib.utils import _config, args2set
from lib.utils.db import confirm_unfound_queue, db

relate_store = db.relation.people_save
relate_query = db.relation.people_find

account_seed = _config['account_seed']
tokens = _config['twitter']


def store_with_friends(user, friends):
    people = {
        'uid': user.id,
        'account': user.screen_name,
        'username': user.name,
        'protect': user.protected,
        'friends_count': user.friends_count,
        'friends': friends
    }
    relate_store(**people)


def store_relation(twitter, uid=None):
    twitter.get_friends(store_with_friends)


def get_seed_people(account_seed):
    people = relate_query(account=account_seed)
    if not people:
        Twitter(**tokens[0]) \
            .get_user(account=account_seed) \
            .get_friends(store_with_friends)
        people = relate_query(account=account_seed)
    return people


@args2set
def get_crawl_queue(account_seeds):
    friends = []
    founds = db.relation.get_uids()
    for account in account_seeds:
        people = get_seed_people(account)
        friends.extend(people.friends)
    unfounds = confirm_unfound_queue(friends, founds)
    return unfounds


def start_crawling_relation(tokens, unfounds):
    multi_tweecrawl(tokens, unfounds, resolve=store_relation)


def run():
    unfounds = get_crawl_queue(account_seed)
    start_crawling_relation(tokens, unfounds)
