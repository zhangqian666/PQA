# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:16
"""

import time
from bert_base.client import BertClient
from utils.printUtil import printi


def ner_on_work(str_input):
    with BertClient(show_server_config=False, check_version=False, check_length=False, mode='NER') as bc:
        start_t = time.perf_counter()
        str_input_list = list(str_input)
        rst = bc.encode([str_input])
        result = list(rst[0])

        printi('命名实体识别进程 - compete 用时 ： {} s'.format(time.perf_counter() - start_t))

        all_entity = []
        entity_list = []
        entity_list_number = 0

        for every in result:
            if every != 'O':
                entity_list.append(str_input_list[entity_list_number])
            else:
                if len(entity_list) > 0:
                    entity_str = "".join(entity_list)
                    all_entity.append(entity_str)
                    entity_list = []
            entity_list_number += 1

        return all_entity
