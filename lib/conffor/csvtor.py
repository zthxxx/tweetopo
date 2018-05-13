# -*- coding: utf-8 -*-
import pandas as pd

from . import ensure_dir_exist


def separator_filter(item):
    if isinstance(item, str):
        return item.replace('\r', ' ').replace('\n', ' ').replace(',', '-')
    return item


def save_list_csv(data, columns, file):
    for index, line in enumerate(data):
        data[index] = [separator_filter(item) for item in line]
    frame = pd.DataFrame(data, columns=columns)
    ensure_dir_exist(file)
    frame.to_csv(file, columns=columns,
                 encoding='utf-8', header=True, index=False)


def read_list_csv(columns, file):
    frame = pd.read_csv(file, names=columns, header=0, encoding='utf-8')
    datas = frame.values
    return datas
