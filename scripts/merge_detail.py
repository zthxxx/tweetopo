# -*- coding: utf-8 -*-
from conffor import csvtor as csv
from .hit_rules import persons_data, fill_leak
from utils.field import read_hub_persons, _HUB_DETAILS_CSV, \
    _HUB_DETAILS_COLUMNS, _HUB_DETAILS_TITLES


def save_hub_details(filename):
    detail_cols = _HUB_DETAILS_COLUMNS
    titles = _HUB_DETAILS_TITLES
    persons_list = read_hub_persons()
    focus = fill_leak()
    details = []
    for person in persons_list:
        uid, *ranks = person
        uid = str(int(uid))
        if uid in focus and uid in persons_data:
            datas = [persons_data[uid].get(column) for column in detail_cols]
            details.append((uid, *ranks, *datas))
    csv.save_list_csv(details, titles, filename)


def run():
    save_hub_details(_HUB_DETAILS_CSV)
