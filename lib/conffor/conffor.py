# -*- coding: utf-8 -*-
"""
Some function for read and write json config file.
"""

import json

from . import ensure_dir_exist


def load(file):
    with open(file, 'r', encoding='utf-8') as jsonfile:
        config = json.load(jsonfile, encoding='utf-8')
        return config


def dump(file, config, indent=2):
    ensure_dir_exist(file)
    with open(file, 'w+', encoding='utf-8') as jsonfile:
        json.dump(
            config, jsonfile,
            indent=indent,
            ensure_ascii=False,
            sort_keys=True
        )
