# -*- coding: utf-8 -*-
from conffor import csvtor as csv
from netgraph.net_distribution import DrawDistribution
from utils import _config
from utils.field import _MUTUAL_FRIENDS_FILE, _HUB_USERS_CSV, \
    _MUTUAL_FRIENDS_COLUMNS, _HUB_USERS_COLUMNS


def read_mutual_friends(filename):
    columns = _MUTUAL_FRIENDS_COLUMNS
    return csv.read_list_csv(columns, filename)


def save_hub_persons(nodes, filename):
    columns = _HUB_USERS_COLUMNS
    csv.save_list_csv(nodes, columns, filename)


def run():
    distribute = _config['distribute']
    edges = read_mutual_friends(_MUTUAL_FRIENDS_FILE)
    drawer = DrawDistribution(edges, measure=distribute['measure'])
    drawer.filter_ranks(distribute['threshold'])
    nodes = drawer.get_nodes()
    save_hub_persons(nodes, _HUB_USERS_CSV)
    drawer.plot_networkx()
    drawer.get_measures()
    drawer.plot_rank_pdf_cdf()
