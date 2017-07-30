# -*- coding: utf-8 -*-
import logging
from conffor import csvtor as csv
from netgraph.net_distribution import DrawDistribution
from utils import _config
from utils.field import _MUTUAL_FRIENDS_FILE, _HUB_USERS_CSV, \
    _MUTUAL_FRIENDS_COLUMNS, _HUB_USERS_COLUMNS


def read_mutual_friends():
    columns = _MUTUAL_FRIENDS_COLUMNS
    return csv.read_list_csv(columns, _MUTUAL_FRIENDS_FILE)


def save_hub_persons(nodes, filename):
    columns = _HUB_USERS_COLUMNS
    csv.save_list_csv(nodes, columns, filename)
    logging.info('Save hub person list csv complete')


def run():
    distribute = _config['distribute']
    logging.info('Loading mutual friends csv ...')
    edges = read_mutual_friends()

    logging.info('Friends distribution analysis ...')
    drawer = DrawDistribution(edges, measure=distribute['measure'])
    drawer.filter_ranks(distribute['threshold'])
    nodes = drawer.get_nodes()
    save_hub_persons(nodes, _HUB_USERS_CSV)

    if distribute['plot_graph']:
        logging.info('Ready to plot distribution map ...')
        drawer.plot_networkx()
        drawer.get_measures()
        drawer.plot_rank_pdf_cdf()
