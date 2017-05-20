# -*- coding: utf-8 -*-
import logging
import pandas as pd

def separator_filter(item):
    if isinstance(item, str):
        return item.replace('\r', ' ').replace('\n', ' ').replace(',', '-')
    return item

def save_list_csv(data, columns, file_name):
    for index, line in enumerate(data):
        data[index] = [separator_filter(item) for item in line]
    frame = pd.DataFrame(data, columns=columns)
    frame.to_csv(file_name, columns=columns,
                 encoding='utf-8', header=True, index=False)

def read_list_csv(columns, file_name):
    frame = pd.read_csv(file_name, names=columns, header=0, encoding='utf-8')
    datas = frame.values
    return datas
