import logging
import os
import signal

from daemon import DaemonContext
import lockfile

from lib.conffor import ensure_dir_exist
from lib.utils import _config

signal.signal(signal.SIGHUP, signal.SIG_IGN)


def preserve_logger(handler):
    if isinstance(handler, logging.FileHandler):
        return handler.stream


def stderr_log():
    log = _config['log']
    if log:
        ensure_dir_exist(log)
        stderr = open(log, 'a', encoding='utf-8')
        return stderr


# ref: https://www.python.org/dev/peps/pep-3143
daemon = DaemonContext(
    working_directory=os.getcwd(),
    pidfile=lockfile.FileLock('.tweetopo.pid'),
    stderr=stderr_log(),
    files_preserve=[preserve_logger(h) for h in logging.getLogger().handlers],
    signal_map={
        signal.SIGHUP: None,
        signal.SIGTERM: 'close'
    }
)
