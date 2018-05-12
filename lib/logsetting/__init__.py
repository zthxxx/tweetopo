# -*- coding: utf-8 -*-
"""
Output the log to both log-file and console.
"""
import logging
import os
import sys

from lib.utils import _config

MSG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FILE = _config['log']


def format_stream(stream=sys.stdout,
                  level=logging.INFO, msg_format=MSG_FORMAT, date_format=TIME_FORMAT):
    """
    create a formatted stream handler
    """
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    handler.setFormatter(formatter)
    return handler


def clear_logsetting():
    root = logging.getLogger()
    root.handlers = []
    return root


def reset_logbase(
    filename=LOG_FILE, stream=sys.stdout,
    filemode='a',
    level=logging.INFO, msg_format=MSG_FORMAT, date_format=TIME_FORMAT,
):
    format_config = {
        'level': level,
        'format': msg_format,
        'datefmt': date_format,
        'filemode': filemode
    }
    root = clear_logsetting()
    logging.basicConfig(filename=filename, **format_config)
    if stream:
        root.addHandler(format_stream(stream, **format_config))
    if filename is not LOG_FILE and os.path.isfile(LOG_FILE):
        os.remove(LOG_FILE)
