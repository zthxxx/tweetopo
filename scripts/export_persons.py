# -*- coding: utf-8 -*-
from utils.db import db
from utils.field import get_hub_uids, get_secondouts_uids, _HUB_USERS_JSON


def export_hub_persons(filename):
    hub_uids = get_hub_uids()
    secondout_uids = get_secondouts_uids()
    db.person.export_persons(filename, uids=list(hub_uids | secondout_uids))


def run():
    export_hub_persons(_HUB_USERS_JSON)
