from lib.cli import FlowRange, Separate, cli, click, ops
from lib.utils.config import parse_config
from lib.utils.workflow import workflow

DEFAULTS = {
    'config': 'config/tweetconf.json',
    'token': 'config/twitter-tokens.json',
    'proxy': 'config/proxy.json',
    'log': './output.log',
    'stderr': './error.log',
    'daemon': False
}

ops('--config', metavar='<config-path>', default=DEFAULTS['config'], type=click.Path(exists=True),
    help='set tweetopo config file. Default: %s' % DEFAULTS['config'])
ops('--token', metavar='<token-path>', default=DEFAULTS['token'], type=click.Path(exists=True),
    help='set twitter tokens file. Default: %s' % DEFAULTS['token'])
ops('-u', '--user', metavar='<user[, ...]>', cls=Separate,
    help='set seed user`s names, separated by comma')
ops('--proxy-path', metavar='<path>', default=DEFAULTS['proxy'], type=click.Path(exists=True),
    help='set proxy file, proxy string in json list. Default: %s' % DEFAULTS['proxy'])
ops('-p', '--proxy', metavar='<proxy[, ...]>', cls=Separate,
    help='set proxy uri list, separated by comma. will override `--proxy-path` set.')
ops('-d', '--daemon', is_flag=True, default=DEFAULTS['daemon'],
    help='to trigger the command run in daemon')
ops('--log', metavar='<path>', default=DEFAULTS['log'], type=click.Path(),
    help='set the output log file. Default: %s' % DEFAULTS['log'])
ops('--stderr', metavar='<path>', default=DEFAULTS['stderr'], type=click.Path(),
    help='set the stderr output file. Default: %s' % DEFAULTS['stderr'])
ops('-f', '--flow', metavar='<step>', cls=FlowRange,
    help='set appoint a flow step to run. Default: all; workflows see below: \n' +
         'step\tflowname\n' +
         ''.join(['%s\t%s \n' % (step, name) for step, name in enumerate(workflow)]))


@cli.resultcallback()
def callback_parse_config(_, **options):
    parse_config(options)


cli.help = '''
    tweetopo
    analyse twitter user public tweet data
'''
