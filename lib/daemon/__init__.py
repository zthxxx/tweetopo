import logging
import os
import signal
import sys

from daemon import DaemonContext
import lockfile

from lib.conffor import ensure_dir_exist
from lib.utils import _config

signal.signal(signal.SIGHUP, signal.SIG_IGN)


def preserve_logger(handler):
    if isinstance(handler, logging.FileHandler):
        return handler.stream


def stderr_log():
    err = _config['stderr']
    if err:
        ensure_dir_exist(err)
        stderr = open(err, 'a', encoding='utf-8')
        return stderr


class Daemon(DaemonContext):
    def terminate(self, signal_number, stack_frame):
        self.__exit__(None, None, None)
        sys.exit(0)


# ref: https://www.python.org/dev/peps/pep-3143
daemon = Daemon(
    working_directory=os.getcwd(),
    pidfile=lockfile.FileLock('.tweetopo.pid'),
    stderr=stderr_log(),
    files_preserve=[preserve_logger(h) for h in logging.getLogger().handlers],
    signal_map={
        signal.SIGHUP: None,
        signal.SIGTERM: 'terminate'
    }
)
