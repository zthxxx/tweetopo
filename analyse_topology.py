# -*- coding: utf-8 -*-
import logging

import logsetting
from conffor import conffor
from database import mongo_orm as database


conf_file = './tweetconf.json'
config = conffor.load(conf_file)
database.set_connect(**config["mongo"])

def get_jaccard_between(set_from, set_to):
    if not isinstance(set_from, set):
        set_from = set(set_from)
    if not isinstance(set_to, set):
        set_to = set(set_to)
    score = len(set_from & set_to) / len(set_from | set_to)
    return score
