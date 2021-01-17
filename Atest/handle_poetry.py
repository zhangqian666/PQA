# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2021-01-16 16:45
"""
import pandas as pd

root_data = pd.read_csv("./poetry_list.csv", usecols=["type", "string"])
