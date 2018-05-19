## collection: relation

In mongodb, collection of `relation` stores the relationship for user friends(alias of **followings**), the structure of field defined here.

### document field:

ref docs: 

- https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
- https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids



```js
{
  
  "_id": Number,  // alias `id` in user-object, `uid` in orm,
  "account": String, // alias `screen_name` in user-object
  "username": String, // alias `name` in user-object
  "friends_count": Number,
  "friends": Array<Number>, // alias `friends.ids` in get-friends-ids
  "protect": Boolean // alias `protected` in user-object
}
```

