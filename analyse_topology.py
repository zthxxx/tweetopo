# -*- coding: utf-8 -*-
import logging
import pandas as pd
import logsetting
from conffor import conffor
from netgraph.net_distribution import DrawDistribution

relation_file = './twitter_relations.json'
mutual_friends_file = './mutual_friends.csv'
hub_users_file = './hub_users.csv'
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

def save_list_csv(data, columns, file_name):
    frame = pd.DataFrame(data, columns=columns)
    frame.to_csv(file_name, columns=columns,
                       header=True, index=False)

def read_list_csv(columns, file_name):
    frame = pd.read_csv(file_name, names=columns, header=0)
    datas = frame.values
    return datas

def save_mutual_friends(edges, file_name):
    columns = ['user', 'friend', 'weight']
    save_list_csv(edges, columns, file_name)

def read_mutual_friends(file_name):
    columns = ['user', 'friend', 'weight']
    return read_list_csv(columns, file_name)

def save_hub_users(nodes, file_name):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    save_list_csv(nodes, columns, file_name)

def read_hub_users(file_name):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    return read_list_csv(columns, file_name)

if __name__ == "__main__":
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges, mutual_friends_file)

    edges = read_mutual_friends(mutual_friends_file)
    drawer = DrawDistribution(edges, measure='pagerank')
    drawer.filter_nodes(0.3)
    nodes = drawer.get_nodes()
    save_hub_users(nodes, hub_users_file)
    drawer.plot_networkx()
    drawer.plot_rank_pdf_cdf()
