#!/usr/bin/env python3
import logging
from lib.utils import _config

from .scripts import crawling_relation, export_relation, select_secondout, \
    mutual_friends, select_hub, crawling_detail, export_persons, \
    hit_rules, merge_detail

workflow = [
    crawling_relation,
    export_relation,
    mutual_friends,
    select_hub,
    select_secondout,
    crawling_detail,
    export_persons,
    hit_rules,
    merge_detail
]


def main():
    flow_steps = _config['flow']
    if flow_steps is None:
        flow_steps = range(len(workflow))

    for step in flow_steps:
        logging.info('Next workflow step: %d - %s' % (step, workflow[step].__name__))
        workflow[step].run()


main()
