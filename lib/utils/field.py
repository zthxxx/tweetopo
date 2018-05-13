# -*- coding: utf-8 -*-
from os import path

from lib.conffor import conffor, csvtor as csv
from lib.database.person import PERSON_FIELD
from lib.utils.config import config as _config

_DATA_ROOT = path.join('.', '.process_data', '%s')

_RELATION_FILE = _DATA_ROOT % 'twitter_relations.json'
_SECONDOUTS_CSV = _DATA_ROOT % 'secondouts.csv'
_MUTUAL_FRIENDS_FILE = _DATA_ROOT % 'mutual_friends.csv'
_HUB_USERS_CSV = _DATA_ROOT % 'hub_persons.csv'
_HUB_USERS_JSON = _DATA_ROOT % 'hub_persons.json'
_FOCUS_USERS_CSV = _DATA_ROOT % 'focus_hub.csv'
_FIELD_LANGUAGE_JSON = path.join('field_languages', '%s.json')
_HUB_DETAILS_CSV = _DATA_ROOT % 'hub_details.csv'

_SECONDOUTS_COLUMNS = ['uid', 'repeats']
_MUTUAL_FRIENDS_COLUMNS = ['user', 'friend', 'weight']
_HUB_USERS_COLUMNS = ['uid', 'degree', 'pagerank', 'clustering']
_HUB_DETAILS_COLUMNS = PERSON_FIELD
_FOCUS_USERS_COLUMNS = ['uid', 'rule']

_language = _config['field_language']
_language_file = path.join(path.dirname(__file__), _FIELD_LANGUAGE_JSON % _language)
fields = conffor.load(_language_file)


def read_hub_persons():
    columns = _HUB_USERS_COLUMNS
    return csv.read_list_csv(columns, _HUB_USERS_CSV)


def get_hub_uids():
    hub_persons = read_hub_persons()
    uid_col = _HUB_USERS_COLUMNS.index('uid')
    hub_uids = {int(person[uid_col]) for person in hub_persons}
    return hub_uids


def read_secondouts():
    columns = _SECONDOUTS_COLUMNS
    return csv.read_list_csv(columns, _SECONDOUTS_CSV)


def get_secondouts_uids():
    secondouts = read_secondouts()
    uid_col = _SECONDOUTS_COLUMNS.index('uid')
    secondout_uids = {int(person[uid_col]) for person in secondouts}
    return secondout_uids
