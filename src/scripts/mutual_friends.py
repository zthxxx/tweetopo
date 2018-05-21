import logging

from lib.conffor import conffor, csvtor as csv
from lib.utils import _config, args2set
from lib.utils.field import _MUTUAL_FRIENDS_COLUMNS, _MUTUAL_FRIENDS_FILE, _RELATION_FILE

distribute = _config['distribute']


@args2set
def jaccard_weight_score(set_from, set_to):
    score = len(set_from & set_to) / len(set_from | set_to)
    return score


@args2set
def coincide_weight_score(set_from, set_to):
    score = len(set_from & set_to)
    return score


def disable_weight_score(set_from, set_to):
    return 1


def get_weight_method():
    weight_name = distribute['weight'] or 'disable'
    return globals()['%s_weight_score' % weight_name]


def get_mutual_friends_edges(relations):
    edges = []
    users = set(int(key) for key in relations.keys())
    get_weight = get_weight_method()
    for user, friends in relations.items():
        user = int(user)
        for friend in friends:
            if friend in users:
                friend_friends = relations[str(friend)]
                if user in friend_friends:
                    edges.append((user, friend, get_weight(friends, friend_friends)))
    return edges


def save_mutual_friends(edges, filename):
    columns = _MUTUAL_FRIENDS_COLUMNS
    csv.save_list_csv(edges, columns, filename)
    logging.info('Save mutual friends csv complete')


def run():
    relations = conffor.load(_RELATION_FILE)
    edges = get_mutual_friends_edges(relations)
    save_mutual_friends(edges, _MUTUAL_FRIENDS_FILE)
