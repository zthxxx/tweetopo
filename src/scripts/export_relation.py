# -*- coding: utf-8 -*-
from lib.utils import _config
from lib.utils.db import db
from lib.utils.field import _RELATION_FILE

seed_name = _config['seed_name']


def run():
    db.relation.export_relation(_RELATION_FILE, seed_name=seed_name)
