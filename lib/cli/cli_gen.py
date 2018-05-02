"""
    base on Click

    use ops() os click.option() to add options
    use @cli.resultcallback() to add callback function
"""

import locale

import click

# also set "LC_ALL=en_US.UTF-8" in pycharm environment or system env
# PyCharm -> Run -> Edit Configurations -> Defaults -> Python -> Environment variables
# $ export LC_ALL=en_US.UTF-8
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
click.disable_unicode_literals_warning = True


@click.group(name='tweetopo', invoke_without_command=True, chain=True)
@click.option('--test', is_flag=True, default=False, expose_value=False,
              help='use test config and env')
@click.pass_context
def cli(ctx, **options):
    """
    this is a cli help docs
    """
    if ctx.obj is None:
        ctx.obj = options


def ops(*args, **kwargs):
    click.option(*args, **kwargs)(cli)


# parse params and invoke callback, but not exit
_cli_main = cli.main
cli.main = lambda *args, **kwargs: _cli_main(*args, standalone_mode=False, **kwargs)
