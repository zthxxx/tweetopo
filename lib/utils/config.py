from random import shuffle

from lib.conffor import conffor

config = {}


def hook_daemon(config, daemon):
    if not daemon:
        return
    config['secondouts']['plot_CDF'] = False
    config['distribute']['plot_graph'] = False
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ModuleNotFoundError:
        pass


def hook_proxy(config, proxy, tokens):
    if not proxy:
        return
    shuffle(proxy)
    for i, token in enumerate(tokens):
        token['proxy'] = proxy[i % len(proxy)]
    config['twitter'] = tokens


def parse_config(options):
    tokens = conffor.load(options['token'])
    proxy = options.get('proxy') or conffor.load(options['proxy_path'])
    config.update(conffor.load(options['config']))
    merge = {
        'twitter': tokens,
        'account_seed': options['user'] or config['account_seed'],
        'flow': options.get('flow'),
        'daemon': options['daemon'],
        'log': options['log'],
        'stderr': options['stderr']
    }
    config.update(merge)
    hook_proxy(config, proxy, tokens)
    hook_daemon(config, options['daemon'])
