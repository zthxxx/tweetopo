#!/usr/bin/env bash
# workdir: tweetopo
# source build/build.sh

. build/template-render.sh


tmplt.render config/tweetconf.json \
    config/twitter-tokens.json \
    config/proxy.json \
    config/rules.json \
    config/init-db.js \
    test/database_test/db_unit_test.json

pip --timeout 600 install -r requirements.txt
