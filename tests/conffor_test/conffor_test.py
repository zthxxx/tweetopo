# -*- coding: utf-8 -*-
import logging
import random
import os
from conffor import conffor

JSONFILE = './test.json'

config = {
    'name': 'test',
    'chart': u'中文测试',
    'newline': 'one\ntwo\nthree',
    'random': random.random(),
    'None': None,
    'true': True
}

def conf_write_read_test():
    conffor.dump(JSONFILE, config)
    conf_test = conffor.load(JSONFILE)
    for key in config:
        assert config[key] == conf_test[key]
    logging.info("Test config read and save method OK.")

def teardown_module():
    if os.path.isfile(JSONFILE):
        os.remove(JSONFILE)

if __name__ == '__main__':
    conf_write_read_test()
    teardown_module()
