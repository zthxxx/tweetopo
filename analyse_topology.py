# -*- coding: utf-8 -*-
import logging
import random
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import logsetting
from conffor import conffor

relation_file = './twitter_relations.json'
mutual_friends_file = './mutual_friends.csv'
relations = conffor.load(relation_file)

def get_jaccard_between(set_from, set_to):
    if not isinstance(set_from, set):
        set_from = set(set_from)
    if not isinstance(set_to, set):
        set_to = set(set_to)
    score = len(set_from & set_to) / len(set_from | set_to)
    return score

def get_mutual_friends_edges(relations):
    edges = []
    users = set(int(key) for key in relations.keys())
    for user, friends in relations.items():
        user = int(user)
        for friend in friends:
            if friend in users and user in relations[str(friend)]:
                edges.append((user, friend))
    return np.asarray(edges)

def save_mutual_friends(edges):
    columns = ['user', 'friend']
    edges_frame = pd.DataFrame(edges, columns=columns)
    edges_frame.to_csv(mutual_friends_file, columns=columns,
                   header=False, index=False)

def read_mutual_friends(file_name):
    columns = ['user', 'friend']
    edges = pd.read_csv(file_name, names=columns)
    return np.asarray(edges)

def plot_edges_graph_rand_color(edges):
    if not isinstance(edges, np.ndarray):
        edges = np.asarray(edges)
    graph = nx.Graph()
    graph.add_edges_from(edges)
    pos = nx.spring_layout(graph)
    nx.draw(
        graph, pos,
        node_size=30,
        alpha=0.8,
        with_labels=False
    )
    plt.show()

if __name__ == "__main__":
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges)

    edges = read_mutual_friends(mutual_friends_file)
    plot_edges_graph_rand_color(edges)
