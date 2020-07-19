# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:16
"""

import time
from bert_base.client import BertClient
from utils.printUtil import printi

all_labels = ["B-POE",  # 诗名首字
              "I-POE",  # 诗名其它字
              "B-VER",  # 诗句首字
              "I-VER",  # 诗句其它字
              "B-PEO",  # 人名首字
              "I-PEO",  # 人名其它字
              "B-LOC",  # 地点首字
              "I-LOC",  # 地点其它字
              "B-POT",  # 状物首字
              "I-POT",  # 状物其它字
              "B-DYN",  # 朝代首字
              "I-DYN",  # 朝代其它字
              "B-POC",  # 类别首字
              "I-POC",  # 类别其它字
              "B-POG",  # 体裁首字
              "I-POG",  # 体裁其它字
              ]
entity_labels = ["B-POE",  # 诗名首字
                 "B-VER",  # 诗句首字
                 "B-PEO",  # 人名首字
                 "B-LOC",  # 地点首字
                 "B-POT",  # 状物首字
                 "B-DYN",  # 朝代首字
                 "B-POC",  # 类别首字
                 "B-POG",  # 体裁首字
                 ]


def ner_on_work(question):
    with BertClient(port=5559, port_out=5560, show_server_config=False, check_version=False, check_length=False,
                    mode='NER') as bc:
        start_t = time.perf_counter()
        str_input_list = list(question)
        rst = bc.encode([question])
        question_labels = list(rst[0])

        printi('命名实体识别进程 - compete 用时 ： {} s'.format(time.perf_counter() - start_t))
        all_entity = []
        entity_list = []
        entity_list_number = 0
        current_b_labels = ""
        for labels in question_labels:

            if labels in entity_labels:
                current_b_labels = labels
            if labels != 'O':
                entity_list.append(str_input_list[entity_list_number])
            else:
                if len(entity_list) > 0:
                    entity_str = "".join(entity_list)
                    all_entity.append((current_b_labels, entity_str))
                    entity_list = []

            entity_list_number += 1

        if len(entity_list) > 0:
            entity_str = "".join(entity_list)
            all_entity.append((current_b_labels, entity_str))

        return all_entity
