# -*- coding: utf-8 -*-
from utils import _config
from utils.db import db
from utils.field import _RELATION_FILE

seed_name = _config['seed_name']


def run():
    db.relation.export_relation(_RELATION_FILE, seed_name=seed_name)
