# -*- coding: utf-8 -*-
import logging
import pandas as pd
import logsetting
from conffor import conffor, csvtor as csv
from netgraph.net_distribution import DrawDistribution

relation_file = './twitter_relations.json'
mutual_friends_file = './mutual_friends.csv'
hub_users_csv = './hub_persons.csv'
hub_users_json = './hub_persons.json'
hub_details_csv = './hub_details.csv'
relations = conffor.load(relation_file)

def get_jaccard_between(set_from, set_to):
    if not isinstance(set_from, set):
        set_from = set(set_from)
    if not isinstance(set_to, set):
        set_to = set(set_to)
    score = len(set_from & set_to) / len(set_from | set_to)
    return score

def get_mutual_count(set_from, set_to):
    score = len(set(set_from) & set(set_to))
    return score

def get_mutual_friends_edges(relations):
    edges = []
    users = set(int(key) for key in relations.keys())
    for user, friends in relations.items():
        user = int(user)
        for friend in friends:
            if friend in users:
                friend_friends = relations[str(friend)]
                if user in friend_friends:
                    # weight = get_jaccard_between(friends, friend_friends)
                    # edges.append((user, friend, weight))
                    edges.append((user, friend, 1))
    return edges

def save_mutual_friends(edges, filename):
    columns = ['user', 'friend', 'weight']
    csv.save_list_csv(edges, columns, filename)

def read_mutual_friends(filename):
    columns = ['user', 'friend', 'weight']
    return csv.read_list_csv(columns, filename)

def save_hub_persons(nodes, filename):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    csv.save_list_csv(nodes, columns, filename)

def read_hub_persons(filename):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    return csv.read_list_csv(columns, filename)

def get_hub_uids(filename):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    hub_persons = read_hub_persons(filename)
    uid_col = columns.index('uid')
    hub_uids = {int(person[uid_col]) for person in hub_persons}
    return hub_uids


def save_hub_details(filename):
    detail_cols = ['name', 'fullname', 'description', 'sign_at', 'location','time_zone',
                   'friends_count', 'followers_count', 'statuses_count', 'url', 'protect', 'verified']
    titles = ['ID', '度中心性', 'pagerank', '群聚系数', '用户名', '用户全名', '个人描述', '注册时间',
              '位置', '时区', '正在关注数', '关注者数', '推文数量', '个人页面', '是否保护', '是否认证']
    persons_db = conffor.load(hub_users_json)
    persons_list = read_hub_persons(hub_users_csv)
    details = []

    for person in persons_list:
        uid, *ranks = person
        uid = str(int(uid))
        if uid in persons_db:
            datas = [persons_db[uid].get(column) for column in detail_cols]
            details.append((uid, *ranks, *datas))
    csv.save_list_csv(details, titles, filename)

if __name__ == "__main__":
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges, mutual_friends_file)

    edges = read_mutual_friends(mutual_friends_file)
    drawer = DrawDistribution(edges, measure='pagerank')
    drawer.filter_nodes(0.3)
    nodes = drawer.get_nodes()
    save_hub_persons(nodes, hub_users_csv)
    drawer.plot_networkx()
    drawer.get_measures()
    drawer.plot_rank_pdf_cdf()

    # save_hub_details(hub_details_csv)
