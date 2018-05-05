#!/usr/bin/env bash

__COMMENTS__='
# OS: ubuntu 16.04 trusty
# python: 3.6
# pip: 9.0.1 for python3.6
# sudo: required
# need "CONSUMER_KEY" "CONSUMER_SECRET" "ACCESS_TOKEN" "ACCESS_TOKEN_SECRET" "SEED_NAME" variable in env.
# how to use: in travis, use the script to run:
#    source build/build.sh
'

. build/template-substitution.sh


template_render config/tweetconf.json \
                config/twitter-tokens.json \
                config/proxy.json \
                config/rules.json

sudo apt-get install -y python3 python3-dev python3-pip
pip --timeout 600 install -r requirements.txt
