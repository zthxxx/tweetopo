#!/bin/bash

__COMMENTS__='
# OS: ubuntu 14.04 trusty
# python: 3.5
# pip: 9.0.1 for python3.5
# sudo: required
# need "CONSUMER_KEY" "CONSUMER_SECRET" "ACCESS_TOKEN" "ACCESS_TOKEN_SECRET" "SEED_NAME" variable in env.
# how to use: in travis, use the script to run:
#    souce travis_env_init.sh
'


tweetconf='./tweetconf.json'
cp "${tweetconf}.example" "${tweetconf}"
sed -i'' "s~ACCESS_TOKEN_SECRET~${ACCESS_TOKEN_SECRET}~" "${tweetconf}"
sed -i'' "s~ACCESS_TOKEN~${ACCESS_TOKEN}~" "${tweetconf}"
sed -i'' "s~CONSUMER_SECRET~${CONSUMER_SECRET}~" "${tweetconf}"
sed -i'' "s~CONSUMER_KEY~${CONSUMER_KEY}~" "${tweetconf}"
sed -i'' "s~SEED_NAME~${SEED_NAME}~" "${tweetconf}"

echo "python environment pre install start."
# Scientific computation packages
sudo apt-get install -y python3-dev


echo "python environment pre install complete OK."
