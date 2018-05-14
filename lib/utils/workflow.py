from importlib import import_module

workflow = [
    'crawling_relation',
    'export_relation',
    'mutual_friends',
    'select_hub',
    'select_secondout',
    'crawling_detail',
    'export_persons',
    'hit_rules',
    'merge_detail'
]


def reflect_workflow():
    prefix = 'src.scripts.%s'
    return [import_module(prefix % module) for module in workflow]
