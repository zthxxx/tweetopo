#!/bin/bash

__COMMENTS__='
# OS: ubuntu 14.04 trusty
# python: 3.5
# pip: 9.0.1 for python3.5
# sudo: required
# how to use: in travis, use the script to run:
#    souce travis_env_init.sh
'

echo "python environment pre install start."

# Scientific computation packages
sudo apt-get install -y python3-dev


echo "python environment pre install complete OK."
