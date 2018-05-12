import logging
import os
import signal

from daemon import DaemonContext
import lockfile

signal.signal(signal.SIGHUP, signal.SIG_IGN)


def preserve_logger(handler):
    if isinstance(handler, logging.FileHandler):
        return handler.stream


daemon = DaemonContext(
    working_directory=os.getcwd(),
    pidfile=lockfile.FileLock('.tweetopo.pid'),
    files_preserve=[preserve_logger(h) for h in logging.getLogger().handlers],
    signal_map={
        signal.SIGHUP: None,
        signal.SIGTERM: 'close'
    }
)
