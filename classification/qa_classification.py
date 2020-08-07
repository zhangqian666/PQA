# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-08-06 11:28
"""
from bert_base.client import BertClient


def classif(question):
    bc = BertClient(port=5559, port_out=5560, mode="CLASS")
    result = bc.encode([question])

    return result[0]["pred_label"]
