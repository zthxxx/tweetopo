# -*- coding: utf-8 -*-
import logging
import pandas as pd

def save_list_csv(data, columns, file_name):
    frame = pd.DataFrame(data, columns=columns)
    frame.to_csv(file_name, columns=columns,
                       header=True, index=False)

def read_list_csv(columns, file_name):
    frame = pd.read_csv(file_name, names=columns, header=0)
    datas = frame.values
    return datas
