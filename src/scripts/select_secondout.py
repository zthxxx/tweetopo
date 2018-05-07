from collections import Counter
import logging
from operator import itemgetter as _itemgetter

from lib.conffor import conffor, csvtor as csv
from lib.netgraph.net_distribution import DrawDistribution
from lib.utils import _config
from lib.utils.field import _RELATION_FILE, _SECONDOUTS_COLUMNS, _SECONDOUTS_CSV


def count_up_repeat(relations):
    counter = Counter()
    for seconds in relations.values():
        counter.update(seconds)
    logging.info('All SecondOut friends are total of %d.' % len(counter))
    return counter


def plot_counter_cdf(counter):
    signal = list(counter.values())
    DrawDistribution.plot_cdf(signal)


def secondouts_select(firstouts, counter, pass_threshold):
    pass_count = len(firstouts) * pass_threshold
    secondouts = [(uid, count) for uid, count in counter.items()
                  if count > pass_count and uid not in firstouts]
    logging.info('Select %.1f%% repeats of SecondOuts are %d.' %
                 (pass_threshold * 100, len(secondouts)))
    return sorted(secondouts, key=_itemgetter(1), reverse=True)


def save_secondout_friends(edges, filename):
    columns = _SECONDOUTS_COLUMNS
    csv.save_list_csv(edges, columns, filename)
    logging.info('Save select secondouts friends csv complete')


def run():
    relations = conffor.load(_RELATION_FILE)
    counter = count_up_repeat(relations)
    secondouts_conf = _config['secondouts']
    pass_threshold = secondouts_conf['threshold']
    firstouts = {int(key) for key in relations.keys()}
    logging.info('FirstOut friends of seeds have %d people.' % len(firstouts))
    if secondouts_conf['repetition_CDF']:
        plot_counter_cdf(counter)
    secondouts = secondouts_select(firstouts, counter, pass_threshold)
    save_secondout_friends(secondouts, _SECONDOUTS_CSV)
