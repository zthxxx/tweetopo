# -*- coding: utf-8 -*-
import logging
import random
import os
from conffor import conffor

jsonfile = './test.json'

config = {
    'name': 'test',
    'chart': u'中文测试',
    'newline': 'one\ntwo\nthree',
    'random': random.random(),
    'None': None,
    'true': True
}

def conf_write_read_test():
    conffor.dump(jsonfile, config)
    conf_test = conffor.load(jsonfile)
    if os.path.exists(jsonfile):
        os.remove(jsonfile)
    for key in config:
        assert config[key] == conf_test[key]
    logging.warning("Test config read and save method OK.")

if __name__ == '__main__':
    conf_write_read_test()
