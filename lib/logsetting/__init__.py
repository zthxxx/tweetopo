# -*- coding: utf-8 -*-
"""
Output the log to both log-file and console.
"""
import logging
import os
import sys

from lib.utils import _config

msg_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
log_file = _config['log']

logging.basicConfig(
    level=logging.INFO,
    format=msg_format,
    datefmt=date_format,
    filename=log_file,
    filemode='a'
)


def get_formatted_handler(stream=sys.stdout):
    """
    create a formatted stream handler
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    handler.setFormatter(formatter)
    return handler


# append console to root logger
logging.getLogger().addHandler(get_formatted_handler())


def clean_log_set():
    root = logging.getLogger()
    root.handlers = []


def reset_base(
    level=logging.INFO, format=msg_format, datefmt=date_format,
    filename=log_file, filemode='a', stream=sys.stdout
):
    root = logging.getLogger()
    root.handlers = []
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        filename=filename,
        filemode=filemode
    )
    root.addHandler(get_formatted_handler(stream))
    if filename != log_file and os.path.isfile(log_file):
        os.remove(log_file)
