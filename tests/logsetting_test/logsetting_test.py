# -*- coding: utf-8 -*-
import os
import sys
import filecmp
import logging

redirect_file = './stdout.out'
log_file = './test.log'

def log_reset(console):
    import logsetting
    logsetting.resetbase(filename=log_file, filemode='w', console_stream=console)

def redirect_stdout(callback):
    with open(redirect_file, 'w+', encoding="utf-8") as file:
        sys.stderr = sys.stdout = file
        log_reset(console=file)
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

def logging_test():
    redirect_stdout(loggings)
    recover_stdout()
    compare_logfile_and_stdout()

def clean_outlog():
    from logsetting import clean_log_set
    clean_log_set()
    if os.path.isfile(log_file):
        os.remove(log_file)
    if os.path.isfile(redirect_file):
        os.remove(redirect_file)

def teardown_module():
    recover_stdout()
    clean_outlog()

if __name__ == '__main__':
    logging_test()
    teardown_module()
