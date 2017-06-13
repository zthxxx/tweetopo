# -*- coding: utf-8 -*-
from conffor import csvtor as csv
from database.person import PERSON_FIELD

_RELATION_FILE = '_twitter_relations.json'
_MUTUAL_FRIENDS_FILE = '_mutual_friends.csv'
_HUB_USERS_CSV = '_hub_persons.csv'
_HUB_USERS_JSON = '_hub_persons.json'
_HUB_DETAILS_CSV = '_hub_details.csv'

_MUTUAL_FRIENDS_COLUMNS = ['user', 'friend', 'weight']
_HUB_USERS_COLUMNS = ['uid', 'degree', 'pagerank', 'clustering']
_HUB_DETAILS_COLUMNS = PERSON_FIELD
_HUB_DETAILS_TITLES = ['ID', '度中心性', 'pagerank', '群聚系数', '用户名', '用户全名', '个人描述', '注册时间',
                       '位置', '时区', '正在关注数', '关注者数', '推文数量', '个人页面', '是否保护', '是否认证']


def read_hub_persons():
    columns = _HUB_USERS_COLUMNS
    return csv.read_list_csv(columns, _HUB_USERS_CSV)


def get_hub_uids():
    columns = _HUB_USERS_COLUMNS
    hub_persons = read_hub_persons()
    uid_col = columns.index('uid')
    hub_uids = {int(person[uid_col]) for person in hub_persons}
    return hub_uids
