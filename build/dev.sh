#!/usr/bin/env bash
# workdir: tweetopo
# source build/dev.sh

# if not initialized, build it
if [[ ! -d venv ]]; then
  python3 -m venv venv
  . venv/bin/activate
  . build/build.sh
fi
. venv/bin/activate

# mongo docker init operate
mongo_data="/var/lib/mongo/db"
if [[ ! -w "$mongo_data" ]]; then
  sudo mkdir -p "$mongo_data"
  sudo chown -R $USER "$mongo_data"
fi

if ! docker top mongo &> /dev/null; then
  docker rm mongo
  initdb_file="`pwd`/config/init-db.js"
  docker run -d --rm --name mongo \
    -v "$mongo_data":/data/db \
    -v "$initdb_file":/docker-entrypoint-initdb.d/initdb.js \
    -p 23333:27017 \
    mongo:3.6 --auth
fi
