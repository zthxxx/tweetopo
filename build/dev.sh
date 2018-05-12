#!/usr/bin/env bash
# workdir: tweetopo
# source build/dev.sh

[[ -d venv ]] || python3 -m venv venv
. venv/bin/activate
. build/build.sh

# mongo docker init operate
mongo_data="/var/lib/mongo/db"
sudo mkdir -p "$mongo_data"
sudo chown -R $USER "$mongo_data"
initdb_file="`pwd`/config/init-db.js"

docker top mongo &> /dev/null && exit
docker rm mongo
docker run -d --rm --name mongo \
  -v "$mongo_data":/data/db \
  -v "$initdb_file":/docker-entrypoint-initdb.d/initdb.js \
  -p 23333:27017 \
  mongo:3.6 --auth
