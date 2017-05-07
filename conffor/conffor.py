# -*- coding: utf-8 -*-
import json

def load(path):
    config = None
    with open(path, 'r', encoding="utf-8") as jsonfile:
        config = json.load(jsonfile, encoding="utf-8")
    return config

def dump(path, config):
    with open(path, 'w+', encoding="utf-8") as jsonfile:
        json.dump(
            config, jsonfile,
            indent=2,
            ensure_ascii=False,
            sort_keys=True
        )