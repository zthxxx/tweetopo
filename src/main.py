#!/usr/bin/env python3
import logging

from lib.utils import _config
from lib.utils.workflow import reflect_workflow


def main():
    from lib.utils.db import db
    db.add_log4mongo()

    logging.info('Link Start !!! \n')

    workflow = reflect_workflow()
    flow_steps = _config['flow']
    if flow_steps is None:
        flow_steps = range(len(workflow))

    for step in flow_steps:
        logging.info('Next workflow step: %d - %s' % (step, workflow[step].__name__))
        workflow[step].run()
    logging.info('All workflow run accomplish, then will exit.\n')


def run(as_daemon):
    if not as_daemon:
        return main()
    from lib.daemon import daemon
    with daemon:
        main()


run(_config.get('daemon'))
