import logging

from mongoengine import *

from lib.conffor import conffor
from lib.database import doc2dict


class User(EmbeddedDocument):
    uid = IntField(required=True, primary_key=True)
    account = StringField()
    username = StringField()


class Media(EmbeddedDocument):
    id = IntField()
    type = StringField()
    url = URLField()
    thumb = URLField()


class ReplyTo(EmbeddedDocument):
    id = IntField()
    uid = IntField()
    account = StringField()


class Tweet(Document):
    id = IntField(required=True, primary_key=True)
    uid = IntField()
    account = StringField()
    username = StringField()
    text = StringField()
    mention = ListField(EmbeddedDocumentField(User))
    created = DateTimeField()
    media = ListField(EmbeddedDocumentField(Media))
    reply_count = IntField()
    retweet_count = IntField()
    favorite_count = IntField()
    reply_to = EmbeddedDocumentField(ReplyTo)
    quote_with = IntField()
    meta = {
        'indexes': ['#id']
    }


def tweet_save(id, uid, account, **kwargs):
    tweet = Tweet(id=id, uid=uid, account=account, **kwargs)
    tweet.save()


def tweet_id_find(id):
    if not id:
        return
    tweet = Tweet.objects(id=id).first()
    return tweet


def export_user_tweets(filename, uids=None, limit=None):
    cour = Tweet.objects(**{'uid__in': uids}).limit(limit)
    tweets = {
        uid: []
        for uid in uids
    }
    for tweet in cour:
        tweets[tweet.uid].append({
            **doc2dict(tweet),
            'created': str(tweet.created)
        })
    conffor.dump(filename, tweets, None)
    logging.info('Export tweets of specified users complete.')
