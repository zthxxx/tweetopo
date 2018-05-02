from inspect import isclass
from itertools import chain

from lib.cli import click, cli, ops
from .config import parse_config

DEFAULTS = {
    'config': 'config/tweetconf.json',
    'token': 'config/twitter-tokens.json',
    'proxy': 'config/proxy.json'
}


class Separate(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if not value:
                return
            return value.split(',')
        except Exception:
            print('Separate')
            raise click.BadParameter(value)

    def __repr__(self):
        return 'CSV'


class FlowRange(click.Option):
    def parse_range(self, series):
        parts = list(map(int, series.split('-')))
        if 1 > len(parts) > 2:
            raise click.BadParameter(series)
        if len(parts) == 1:
            return parts
        start, end = parts
        if start > end:
            raise click.BadParameter(series)
        return range(start, end + 1)

    def type_cast_value(self, ctx, value):
        try:
            if not value:
                return
            return chain(*map(self.parse_range, value.split(',')))
        except Exception:
            raise click.BadParameter(value)

    def __repr__(self):
        return 'NUM-Range'


class TypeChose(click.Choice):
    def __init__(self, *choices):
        super().__init__(choices)

    def convert(self, value, param, ctx):
        for choice in self.choices:
            if isclass(choice):
                if isinstance(value, choice):
                    return value
            else:
                if value is choice:
                    return value
                try:
                    return choice(value, param, ctx)
                except Exception:
                    print('is not this type', type(choice))
                    pass
        else:
            raise click.BadParameter(value)


ops('--config', metavar='<config-path>', default=DEFAULTS['config'], type=click.Path(exists=True),
    help='set tweetopo config file. Default: %s' % DEFAULTS['config'])
ops('--token', metavar='<token-path>', default=DEFAULTS['token'], type=click.Path(exists=True),
    help='set twitter tokens file. Default: %s' % DEFAULTS['token'])
ops('-u', '--user', metavar='<user[, ...]>', cls=Separate,
    help='set seed users, separated by comma')
ops('--proxy-path', metavar='<path>', default=DEFAULTS['proxy'], type=click.Path(exists=True),
    help='set proxy file, proxy string in json list. Default: %s' % DEFAULTS['proxy'])
ops('-p', '--proxy', metavar='<proxy[, ...]>', cls=Separate,
    help='set proxy uri list, separated by comma. will override `--proxy-path` set.')
ops('-f', '--flow', metavar='<step>', cls=FlowRange,
    help='set appoint a flow step to run. Default: all')

@cli.resultcallback()
def callback_parse_config(_, **options):
    parse_config(options)


cli.help = '''
    tweetopo
    analyse twitter user public tweet data
'''
