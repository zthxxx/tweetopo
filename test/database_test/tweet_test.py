from datetime import datetime
import os
from random import randint

from lib.database.tweet import Tweet, \
    export_user_tweets as export, \
    tweet_id_find as query, \
    tweet_save as store

id_base = randint(344422, 6344422)
uid_base = randint(86344422, 986344422)

TWEETS_COUNT = 5
EXPORT_STORE_FILE = './twitter_tweets.test.json'


def mock_tweet(id, uid):
    return {
        'id': id,
        'uid': uid,
        'account': 'testname',
        'username': 'Test Full name',
        'text': 'This a mock tweet text.',
        'mention': [{
            'uid': uid + 1,
            'account': 'other_account',
            'username': 'other username',
        }],
        'created': datetime.now(),
        'media': [{
            'id': randint(10086, 12315),
            'type': 'video',
            'url': 'https://twitter.com/video/id/xxx'
        }],
        'reply_count': 4,
        'retweet_count': 8,
        'favorite_count': 6
    }


def tweet_field_save(field):
    store(**field)


def test_save_many_same():
    tweet = mock_tweet(id_base, uid_base)
    tweet_field_save(tweet)
    tweet_field_save(tweet)
    tweet_field_save(tweet)
    assert Tweet.objects().count() is 1
    # It should save as only one, and not raise error.


def test_save_many_diff():
    for i in range(0, TWEETS_COUNT):
        tweet_field_save(mock_tweet(id_base + i, uid_base))
        assert Tweet.objects().count() == 1 + i


def test_tweet_find():
    index = id_base
    for i in range(0, TWEETS_COUNT):
        tweet = query(id=index + i)
        assert tweet.uid == uid_base


def test_tweet_read_all():
    index = id_base
    for tweet in Tweet.objects().order_by('id'):
        assert tweet.id == index
        index += 1


def test_export_tweet_collection():
    export(EXPORT_STORE_FILE, uids=[uid_base], limit=10)


def test_tweet_del_all():
    for tweet in Tweet.objects():
        tweet.delete()
    assert Tweet.objects().count() is 0


def teardown_module():
    Tweet.drop_collection()
    if os.path.isfile(EXPORT_STORE_FILE):
        os.remove(EXPORT_STORE_FILE)


if __name__ == '__main__':
    test_save_many_same()
    test_save_many_diff()
    test_tweet_find()
    test_tweet_read_all()
    test_export_tweet_collection()
    test_tweet_del_all()
    teardown_module()
