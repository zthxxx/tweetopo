# -*- coding: utf-8 -*-
from utils.db import db
from conffor import conffor, csvtor as csv
from utils.field import read_hub_persons, get_hub_uids, _HUB_USERS_JSON, \
    _HUB_DETAILS_CSV,  _HUB_DETAILS_COLUMNS, _HUB_DETAILS_TITLES


def export_hub_persons(filename):
    hub_uids = get_hub_uids()
    db.person.export_persons(filename, uids=list(hub_uids))


def save_hub_details(filename):
    detail_cols = _HUB_DETAILS_COLUMNS
    titles = _HUB_DETAILS_TITLES
    persons_db = conffor.load(_HUB_USERS_JSON)
    persons_list = read_hub_persons()
    details = []

    for person in persons_list:
        uid, *ranks = person
        uid = str(int(uid))
        if uid in persons_db:
            datas = [persons_db[uid].get(column) for column in detail_cols]
            details.append((uid, *ranks, *datas))
    csv.save_list_csv(details, titles, filename)

def run():
    export_hub_persons(_HUB_USERS_JSON)
    save_hub_details(_HUB_DETAILS_CSV)
