# -*- coding: utf-8 -*-
import logging
import pandas as pd
import logsetting
from conffor import conffor, csvtor as csv
from netgraph.net_distribution import DrawDistribution

relation_file = './twitter_relations.json'
mutual_friends_file = './mutual_friends.csv'
hub_users_file = './hub_persons.csv'
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

if __name__ == "__main__":
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges, mutual_friends_file)

    edges = read_mutual_friends(mutual_friends_file)
    drawer = DrawDistribution(edges, measure='pagerank')
    drawer.filter_nodes(0.3)
    nodes = drawer.get_nodes()
    save_hub_persons(nodes, hub_users_file)
    drawer.plot_networkx()
    drawer.plot_rank_pdf_cdf()
