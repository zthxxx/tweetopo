# -*- coding: utf-8 -*-
"""
Output the log to both log-file and console.
"""
import os
import sys
import logging

msg_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
log_file = './output.log'

logging.basicConfig(
    level=logging.INFO,
    format=msg_format,
    datefmt=date_format,
    filename=log_file,
    filemode='a'
)

def get_console_stream(stream=None):
    # get and set console log config
    if not stream:
        stream = sys.stdout
    console = logging.StreamHandler(stream)
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    return console

# append console to root logger
logging.getLogger().addHandler(get_console_stream())

def clean_log_set():
    root = logging.getLogger()
    root.handlers = []

def resetbase(
    level=logging.INFO, format=msg_format, datefmt=date_format,
    filename=log_file, filemode='a', console_stream=None
):
    root = logging.getLogger()
    root.handlers=[]
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        filename=filename,
        filemode=filemode
    )
    root.addHandler(get_console_stream(console_stream))
    if filename != log_file and os.path.isfile(log_file):
        os.remove(log_file)
