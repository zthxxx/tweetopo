# -*- coding: utf-8 -*-
from lib.utils import _config
from lib.utils.db import db
from lib.utils.field import _RELATION_FILE

account_seed = _config['account_seed']


def run():
    db.relation.export_relation(_RELATION_FILE, account_seed=account_seed)
