# -*- coding: utf-8 -*-
import logging
import os
from random import randint

from lib.conffor import csvtor as csv

CSVFILE = './test.csv'
COLUMNS = ['name', 'node', 'to', 'weight']

data_list = [['new\r\nline,and comma', randint(0, 5), randint(0, 5), randint(0, 5)] for i in range(0, 5)]


def test_csv_write_read():
    csv.save_list_csv(data_list, COLUMNS, CSVFILE)
    data = csv.read_list_csv(COLUMNS, CSVFILE)
    for index, item in enumerate(data):
        name, *edge = item
        edge = [int(value) for value in edge]
        assert name == data_list[index][0]
        assert edge == data_list[index][1:]
    logging.info("Test csv read and save method OK.")


def teardown_module():
    if os.path.isfile(CSVFILE):
        os.remove(CSVFILE)


if __name__ == '__main__':
    test_csv_write_read()
    teardown_module()
