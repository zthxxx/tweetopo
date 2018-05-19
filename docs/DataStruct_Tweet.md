## collection: tweet

In mongodb, collection of `tweet` stores the tweet which in twitter, the structure of field defined here.

### document field:

ref docs:

- https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
- https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
- https://developer.twitter.com/en/docs/tweets/search/guides/premium-operators

```js
{
    "_id": Number,      // alias `id` in tweet-object, `id` in orm,
    "uid": Number,      // alias `id` in user-object
    "account": String,  // alias `screen_name` in user-object
    "username": String, // alias `name` in user-object"
    "text": String,
    "created": Date,  // alias `created_at` in tweet-object
    "reply_count": Number,
    "retweet_count": Number,
    "favorite_count": Number,
    "mention": [{       // mean `entities.user_mentions` in tweet-object
        "uid": Number,  // alias `id` in user-object
        "account": String, // alias `screen_name` in user-object
        "username": String // alias `name` in user-object"
    }],
    "reply_to": {
        "id": Number,   // id with replied tweet-object
        "uid": Number,  // alias `id` in user-object
        "account": String   // alias `screen_name` in user-object
    },
    "hashtag": Array(String)    // mean `entities.hashtag.text` in tweet-object,
    "quote_with": Number,   // alias `quoted_status_id` in tweet-object
    "media": [{         // mean `extended_entities.media` in tweet-object
        "id": Number,   // the media id in tweet entities.media
        "type": String,
        // alias `media_url_https` in photo media,
        // alias `video_info.variants[bitrate=2176000].url`
        "url": String,
        "thumb": String // alias `media_url_https`
    }]
}
```

