# -*- coding: utf-8 -*-
from lib.utils.db import db
from lib.utils.field import _HUB_USERS_JSON, get_hub_uids, get_secondouts_uids


def export_hub_persons(filename):
    hub_uids = get_hub_uids()
    secondout_uids = get_secondouts_uids()
    db.person.export_persons(filename, uids=hub_uids | secondout_uids)


def run():
    export_hub_persons(_HUB_USERS_JSON)
