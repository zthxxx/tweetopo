# -*- coding: utf-8 -*-
import logging
from conffor import csvtor as csv
from .hit_rules import persons_data
from utils.field import fields, read_hub_persons, _HUB_DETAILS_CSV, \
    _HUB_DETAILS_COLUMNS, _HUB_USERS_COLUMNS, _FOCUS_USERS_CSV, _FOCUS_USERS_COLUMNS


def read_focus_hub():
    columns = _FOCUS_USERS_COLUMNS
    lines = csv.read_list_csv(columns, _FOCUS_USERS_CSV)
    focus = {uid: rule for uid, rule in lines}
    return focus


def filter_persons_unfocus():
    focus = read_focus_hub()
    persons_list = read_hub_persons()
    result = [(uid, *ranks, focus[uid]) for uid, *ranks in persons_list if uid in focus]
    columns = _HUB_USERS_COLUMNS + _FOCUS_USERS_COLUMNS[1:]
    return result, columns


def merge_hub_details(filename):
    detail_cols = _HUB_DETAILS_COLUMNS[1:]
    user_lines, user_columns = filter_persons_unfocus()
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
