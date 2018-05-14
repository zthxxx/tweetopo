#!/usr/bin/env python3
import logging

from lib.utils import _config
from lib.utils.workflow import reflect_workflow


def main():
    workflow = reflect_workflow()
    flow_steps = _config['flow']
    if flow_steps is None:
        flow_steps = range(len(workflow))

    for step in flow_steps:
        logging.info('Next workflow step: %d - %s' % (step, workflow[step].__name__))
        workflow[step].run()
    logging.info('All workflow run accomplish, then will exit.')


def run(as_daemon):
    logging.info('Link Start !!! \n')
    if not as_daemon:
        main()
        return
    from lib.daemon import daemon
    with daemon:
        main()


run(_config.get('daemon'))
