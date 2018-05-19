## collection: person

In mongodb, collection of `person` stores the information which from twitter api of user info details, the structure of field defined there.

### document field:

ref: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

```js
{
  "_id": Number,  // alias `id` in user-object, `uid` in orm,
  "account": String, // alias `screen_name` in user-object
  "username": String, // alias `name` in user-object
  "description": String,
  "avatar": String, // alias `profile_image_url_https` in user-object
  "url": String,
  "sign_at": Date, // alias `created_at` in user-object
  "location": String,
  "time_zone": String,
  "friends_count": Number,
  "followers_count": Number, 
  "followers_count": Number,
  "statuses_count": Number, 
  "favourites_count": Number,
  "protect": Boolean // alias `protected` in user-object
  "verified": Boolean
}
```

