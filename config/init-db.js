const users = {
  dev: {
    name: "kk",
    pwd: "tweet-${MONGO_PASSWD}",
    db: "tweetopo"
  },
  test: {
    name: "unit",
    pwd: "UnitTest-${MONGO_TEST_PASSWD}",
    db: "UnitTest"
  }
}

function newUser(user) {
  db = db.getSiblingDB(user.db)
  if (!db.getUser(user.name)) {
    db.createUser({
      user: user.name,
      pwd: user.pwd,
      roles: [{
        db: user.db,
        role: "readWrite"
      }]
    })
  }
}

newUser(users.dev)
newUser(users.test)
