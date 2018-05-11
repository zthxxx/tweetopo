# -*- coding: utf-8 -*-
import filecmp
import logging
import os
import sys

redirect_file = './stdout.out'
log_file = './test.log'


def log_reset(stream):
    from lib import logsetting
    logsetting.reset_base(filename=log_file, filemode='w', stream=stream)


def redirect_stdout(callback):
    with open(redirect_file, 'w+', encoding='utf-8') as file:
        sys.stderr = sys.stdout = file
        log_reset(file)
        if callable(callback):
            callback()


def loggings():
    logging.debug('This is a debut log')
    logging.info('This is a info log')
    logging.warning('This is a waring log')
    logging.error('This is a error log')


def recover_stdout():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def compare_logfile_and_stdout():
    assert filecmp.cmp(log_file, redirect_file)


def test_logging():
    redirect_stdout(loggings)
    recover_stdout()
    compare_logfile_and_stdout()


def clean_outlog():
    from lib.logsetting import clean_log_set
    clean_log_set()
    if os.path.isfile(log_file):
        os.remove(log_file)
    if os.path.isfile(redirect_file):
        os.remove(redirect_file)


def teardown_module():
    recover_stdout()
    clean_outlog()


if __name__ == '__main__':
    test_logging()
    teardown_module()
