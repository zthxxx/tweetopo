from lib.twitter.tweeapi import multi_tweecrawl
from lib.utils import _config
from lib.utils.db import confirm_unfound_queue, db
from lib.utils.field import get_hub_uids, get_secondouts_uids

from .merge_detail import read_focus_hub

tweet_store = db.tweet.tweet_save

account_seed = _config['account_seed']
tokens = _config['twitter']


def map_tweet_base(tweet):
    return {
        'id': tweet.id,
        'uid': tweet.user.id,
        'account': tweet.user.screen_name,
        'username': tweet.user.name,
        'text': tweet.text,
        'created': tweet.created_at,
        'retweet_count': tweet.retweet_count,
        'favorite_count': tweet.favorite_count,
    }


def map_tweet_premium(tweet):
    if not hasattr(tweet, 'reply_count'):
        return {}
    return {
        'reply_count': tweet.reply_count,
        'quote_count': tweet.quote_count,
    }


def map_tweet_hashtag(tweet):
    if not tweet.entities['hashtags']:
        return {}
    return {
        'hashtags': [hashtag['text'] for hashtag in tweet.entities['hashtags']]
    }


def map_tweet_mention(tweet):
    if not tweet.entities['user_mentions']:
        return {}
    return {
        'mention': [
            {
                'uid': user['id'],
                'account': user['screen_name'],
                'username': user['name'],
            } for user in tweet.entities['user_mentions']
        ]
    }


def map_tweet_reply(tweet):
    if not tweet.in_reply_to_status_id:
        return {}
    return {
        'reply_to': {
            'id': tweet.in_reply_to_status_id,
            'uid': tweet.in_reply_to_user_id,
            'account': tweet.in_reply_to_screen_name,
        }
    }


def map_tweet_retweet(tweet):
    if not hasattr(tweet, 'retweeted_status'):
        return {}
    store_status(tweet.retweeted_status)
    return {
        'retweet_with': tweet.retweeted_status.id
    }


def map_tweet_quote(tweet):
    if not hasattr(tweet, 'quoted_status'):
        return {}
    store_status(tweet.quoted_status)
    return {
        'quote_with': tweet.quoted_status_id
    }


def map_tweet_media(tweet):
    if not hasattr(tweet, 'extended_entities'):
        return {}

    def extract_video(media):
        variants = media['video_info']['variants']
        video = sorted(variants, key=lambda item: item.get('bitrate', 0), reverse=True)[0]
        return video['url']

    medias = tweet.extended_entities['media']
    return {
        'media': [
            {
                'id': media['id'],
                'type': media['type'],
                'thumb': media['media_url_https'],
                'url': (extract_video(media)
                        if 'video_info' in media
                        else media['media_url_https'])
            } for media in medias
        ]
    }


def map_status_tweet(status):
    return {
        **map_tweet_base(status),
        **map_tweet_premium(status),
        **map_tweet_hashtag(status),
        **map_tweet_mention(status),
        **map_tweet_reply(status),
        **map_tweet_retweet(status),
        **map_tweet_quote(status),
        **map_tweet_media(status)
    }


def store_status(status):
    tweet_store(**map_status_tweet(status))


def store_tweet_details(twitter, uid=None):
    twitter.get_timeline(lambda statuses: list(map(store_status, statuses)))


def start_fetch_tweets(tokens, uids):
    multi_tweecrawl(tokens, uids, resolve=store_tweet_details)


def fetch_tweets_from_hub():
    hub_uids = get_hub_uids()
    secondout_uids = get_secondouts_uids()
    uids = confirm_unfound_queue(hub_uids | secondout_uids, set())
    start_fetch_tweets(tokens, uids)


def fetch_tweets_from_focus():
    focus = read_focus_hub()
    uids = list(focus)
    start_fetch_tweets(tokens, uids)


def run():
    # fetch_tweets_from_hub()
    fetch_tweets_from_focus()
