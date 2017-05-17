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
                    # weight = get_mutual_count(friends, friend_friends)
                    edges.append((user, friend, 1))
    return edges

def save_mutual_friends(edges):
    columns = ['user', 'friend', 'weight']
    edges_frame = pd.DataFrame(edges, columns=columns)
    edges_frame.to_csv(mutual_friends_file, columns=columns,
                   header=True, index=False)

def read_mutual_friends(file_name):
    columns = ['user', 'friend', 'weight']
    edges_frame = pd.read_csv(file_name, names=columns, header=0)
    edges = edges_frame.values
    return edges

def save_hub_users(nodes):
    columns = ['uid', 'degree', 'pagerank', 'clustering']
    nodes_frame = pd.DataFrame(nodes, columns=columns)
    nodes_frame.to_csv(hub_users_file, columns=columns,
                   header=True, index=False)

if __name__ == "__main__":
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges)

    edges = read_mutual_friends(mutual_friends_file)
    drawer = DrawDistribution(edges)
    drawer.filter_nodes(0.2)
    nodes = drawer.get_nodes()
    save_hub_users(nodes)
    drawer.plot_networkx()
