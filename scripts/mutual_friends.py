# -*- coding: utf-8 -*-
import logging
from conffor import conffor, csvtor as csv
from utils.field import _RELATION_FILE, _MUTUAL_FRIENDS_FILE, _MUTUAL_FRIENDS_COLUMNS


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
    columns = _MUTUAL_FRIENDS_COLUMNS
    csv.save_list_csv(edges, columns, filename)
    logging.info('Save mutual friends csv complete')


def run():
    relations = conffor.load(_RELATION_FILE)
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges, _MUTUAL_FRIENDS_FILE)
