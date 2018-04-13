In mongodb, collection of `relation` stores the relationship for user followings, the structure of field defined here:

```js
// relation collection
{
  "name": String, // twitter api user screen_name
  "_id": Number,  // twitter api user id, primary key in this collection
  "friends_count": Number, // twitter api user friends_conut
  "friends": Array<Number>, // list of user`s friends id
  "protect": Boolean // flag means people has protect his info
}
```

