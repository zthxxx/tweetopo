In mongodb, collection of `person` stores the information which from twitter api of user info, the structure of field defined there:

```json
// person collection
{
  "name": String, // twitter api user screen_name
  "uid": Number,  // twitter api user id
  "friends_count": Number, // twitter api user friends_conut
  "friends": Array<Number> // list of user`s friends id 
}
```

