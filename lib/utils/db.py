# -*- coding: utf-8 -*-
import logging
import queue

import lib.database as db
from lib.utils.config import config

db_conf = config['mongo']
db.set_connect(**db_conf)


def confirm_unfound_queue(total, founds):
    unfound_set = set(total) - set(founds)
    logging.info('Remaining amount of people is %d' % len(unfound_set))
    unfounds = queue.Queue()
    for uid in unfound_set:
        unfounds.put(uid)
    return unfounds
