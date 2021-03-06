# -*- coding: utf-8 -*-
import logging

from lib.conffor import conffor, csvtor as csv
from lib.utils.field import _FOCUS_USERS_COLUMNS, _FOCUS_USERS_CSV, \
    _HUB_DETAILS_COLUMNS, _HUB_DETAILS_CSV, _HUB_USERS_COLUMNS, \
    _HUB_USERS_JSON, fields, read_hub_persons, read_secondouts


def read_focus_hub():
    columns = _FOCUS_USERS_COLUMNS
    lines = csv.read_list_csv(columns, _FOCUS_USERS_CSV)
    focus = {uid: rule for uid, rule in lines}
    return focus


def read_secondouts_all():
    lines = read_secondouts()
    secondouts_all = {uid: repeats for uid, repeats in lines}
    return secondouts_all


def filter_persons_unfocus():
    focus = read_focus_hub()
    firstouts_all = read_hub_persons()
    secondouts_all = read_secondouts_all()
    firstouts = [(uid, *ranks, focus[uid])
                 for uid, *ranks in firstouts_all if uid in focus]
    ranks_length = len(_HUB_USERS_COLUMNS[1:])
    secondouts = [(uid, *(None,) * ranks_length, repeats)
                  for uid, repeats in secondouts_all.items() if uid in focus]
    columns = _HUB_USERS_COLUMNS + _FOCUS_USERS_COLUMNS[1:]
    return columns, firstouts + secondouts


def merge_hub_details(filename):
    persons_data = conffor.load(_HUB_USERS_JSON)
    detail_cols = _HUB_DETAILS_COLUMNS[1:]
    user_columns, user_lines = filter_persons_unfocus()
    titles = [fields[column] for column in user_columns + detail_cols]
    details = []
    for person in user_lines:
        uid, *ranks = person
        uid = str(int(uid))
        if uid in persons_data:
            datas = [persons_data[uid].get(column) for column in detail_cols]
            details.append((uid, *ranks, *datas))
    csv.save_list_csv(details, titles, filename)
    logging.info('Merge hub focus details csv complete.')


def run():
    merge_hub_details(_HUB_DETAILS_CSV)
