from random import shuffle

from lib.conffor import conffor

config = {}


def parse_config(options):
    tokens = conffor.load(options['token'])
    proxy = options.get('proxy') or conffor.load(options['proxy_path'])
    if proxy:
        shuffle(proxy)
        for i, token in enumerate(tokens):
            token['proxy'] = proxy[i % len(proxy)]
    merge = {
        'twitter': tokens,
        'proxy': proxy,
        'flow': options.get('flow')
    }
    config.update(merge)
    config.update(conffor.load(options['config']))
    if config.get('user'):
        config['seed_name'] = config['user']
