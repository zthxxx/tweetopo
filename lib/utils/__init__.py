from collections import Iterable

from .args import cli
from .config import config as _config

cli()


def ensure_set(data):
    if not isinstance(data, Iterable):
        return {data}
    if not isinstance(data, set):
        return set(data)
    return data


def args2set(func):
    def args_set_func(*args):
        sets = [ensure_set(arg) for arg in args]
        return func(*sets)

    return args_set_func
