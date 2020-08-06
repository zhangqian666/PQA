# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-08-06 11:28
"""
from bert_base.client import BertClient


def classif(question):
    bc = BertClient(port=6666, port_out=6667, mode="CLASS")
    result = bc.encode([question])

    return result[0]["pred_label"]
