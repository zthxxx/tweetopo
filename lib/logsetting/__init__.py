# -*- coding: utf-8 -*-
"""
Output the log to both log-file and console.
"""
import logging
import sys

from lib.conffor import ensure_dir_exist

MSG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


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
    filename=None, stream=sys.stdout,
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
    if filename:
        ensure_dir_exist(filename)
        logging.basicConfig(filename=filename, **format_config)
    if stream:
        root.addHandler(format_stream(stream, level, msg_format, date_format))
