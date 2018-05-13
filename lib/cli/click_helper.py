from inspect import isclass
from itertools import chain

import click


class Separate(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if not value:
                return
            return value.split(',')
        except Exception:
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
                    pass
        else:
            raise click.BadParameter(value)
