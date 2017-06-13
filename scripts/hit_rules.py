# -*- coding: utf-8 -*-
from conffor import conffor
from utils.field import get_hub_uids, _RELATION_FILE, _HUB_USERS_JSON
from utils.focus import pickup, match_focus

persons_data = conffor.load(_HUB_USERS_JSON)
relations = conffor.load(_RELATION_FILE)
focus_columns = ['name', 'fullname', 'description', 'location', 'time_zone']


def hit_focus():
    hits = set()
    for uid, person in persons_data.items():
        # person['focus'] = False
        for column in focus_columns:
            if match_focus(person[column]):
                # person['focus'] = True
                hits.add(uid)
                break
    return hits


def filter_relation(hub):
    filted = {uid: friends for uid, friends in relations.items()
              if uid in hub}
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
    hits = hit_focus()
    omissions = get_hub_uids() - hits
    picks = set()
    if pickup["measure"] == "degree":
        picks = pick_degree(hits, omissions, pickup["threshold"])
    return hits | picks
