#!/usr/bin/env bash

__COMMENTS__='
# OS: ubuntu 14.04 trusty
# python: 3.5
# pip: 9.0.1 for python3.5
# sudo: required
# need "CONSUMER_KEY" "CONSUMER_SECRET" "ACCESS_TOKEN" "ACCESS_TOKEN_SECRET" "SEED_NAME" variable in env.
# how to use: in travis, use the script to run:
#    source travis_env_init.sh
'

compile_template() {
  for target in "$@"; do
eval "cat <<-EOF
$(cat ${target}.template)
EOF" > ${target}
  done
}

compile_template config/tweetconf.json config/rules.json

sudo apt-get install -y python3 python3-dev python3-pip
pip install -r requirements.txt --timeout 600

