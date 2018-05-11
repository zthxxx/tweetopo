#!/usr/bin/env bash

__COMMENTS__='
# OS: ubuntu 16.04 trusty
# python: 3.6
# pip: 9.0.1 for python3.6
# sudo: required
# how to use: in travis, use the script to run:
#    source build/build.sh
'

. build/template-substitution.sh


template_render config/tweetconf.json \
                config/twitter-tokens.json \
                config/proxy.json \
                config/rules.json \
                build/init-db.js \
                test/database_test/db_unit_test.json

pip --timeout 600 install -r requirements.txt
