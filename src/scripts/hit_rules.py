# -*- coding: utf-8 -*-
import logging

from lib.conffor import conffor, csvtor as csv
from lib.utils.field import _FOCUS_DETAIL_FIELD, _FOCUS_USERS_COLUMNS, \
    _FOCUS_USERS_CSV, _HUB_USERS_JSON, _RELATION_FILE, get_hub_uids
from lib.utils.focus import match_focus, pickup

focus_columns = _FOCUS_DETAIL_FIELD


def hit_focus():
    hits = set()
    persons_data = conffor.load(_HUB_USERS_JSON)
    for uid, person in persons_data.items():
        # person['focus'] = False
        for column in focus_columns:
            if match_focus(person.get(column)):
                # person['focus'] = True
                hits.add(int(uid))
                break
    return hits


def filter_relation(hub):
    relations = conffor.load(_RELATION_FILE)
    filted = {int(uid): friends for uid, friends in relations.items()
              if int(uid) in hub}
    return filted


def pick_degree(hits, omissions, threshold):
    picks = set()
    threshold_count = len(hits) * threshold
    omits_relations = filter_relation(omissions)
    for uid, friends in omits_relations.items():
        if len(set(friends) & hits) > threshold_count:
            picks.add(uid)
    return picks


def fill_leak():
    hubs = get_hub_uids()
    hits = hit_focus()
    omissions = hubs - hits
    logging.info('Firstout hubs count: %d, hits in rule: %d, omits: %d' %
                 (len(hubs), len(hits & hubs), len(omissions)))
    logging.info('Hit rule with secondouts total: %d' % len(hits - hubs))
    picks = set()
    if pickup['measure'] == 'degree':
        picks = pick_degree(hits, omissions, pickup['threshold'])
    logging.info('Re pick up firstouts total of %d' % len(picks))
    return hits, picks


def save_focus():
    hits, picks = fill_leak()
    focus = [(uid, 'key') for uid in hits]
    focus.extend([(uid, 'pick') for uid in picks])
    columns = _FOCUS_USERS_COLUMNS
    csv.save_list_csv(focus, columns, _FOCUS_USERS_CSV)
    logging.info('Save focus hub csv complete')


def run():
    save_focus()
