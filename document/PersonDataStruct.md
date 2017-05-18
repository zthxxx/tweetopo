In mongodb, collection of `person` stores the information which from twitter api of user info details, the structure of field defined there:

```json
// person collection
{
  "name": String, // twitter api user screen_name
  "fullname": String, // The name of the user, as they’ve defined it. Not necessarily a person’s name. Typically capped at 20 characters, but subject to change.
  "_id": Number,  // twitter api user id, primary key in this collection
  "description": String, // The user-defined UTF-8 string describing their account.
  "sign_at": Date, // The UTC datetime that the user account was created on Twitter. 
  "location": String, // The user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable. This field will occasionally be fuzzily interpreted by the Search service. 
  "time_zone": String, // A string describing the Time Zone this user declares themselves within.
  "friends_count": Number, // twitter api user friends_conut
  "followers_count": Number, // The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate “0”
  "statuses_count": Number, // twitter api user friends_conut
  "friends": Array<Number>, // list of user`s friends id
  "url": String, // A URL provided by the user in association with their profile. 
  "protect": Boolean // When true, indicates that this user has chosen to protect their Tweets. 
  "verified": Boolean // When true, indicates that the user has a verified account.
}
```



> https://dev.twitter.com/overview/api/users