# -*- coding: utf-8 -*-
"""
Output the log to both log-file and console.
"""
import logging

log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=datefmt,
    filename='./tweetopo.log',
    filemode='a'
)

console = logging.StreamHandler()
formatter = logging.Formatter(fmt=log_format,datefmt=datefmt)
# set console log config
console.setLevel(logging.INFO)
console.setFormatter(formatter)
# append console to root logger
logging.getLogger('').addHandler(console)
