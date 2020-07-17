# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 13:32
"""
from EL.data.ner import ner_on_work
from gstore_set.query_model import Model as GstoreQueryModel
from utils.printUtil import *


def el(question):
    """
    启动 BERT-BiLSTM-CRF-NER 服务 用于 命名实体识别
    也就是启动 /EL/ber_server/bert_server_ner.sh

    :return: { 实体名称 : 候选属性列表}
    """
    ner_content = ner_on_work(question)

    gstoreQueryModel = GstoreQueryModel()

    ner_attr_dict = {}

    for entity_item in ner_content:
        if len(gstoreQueryModel.parse_json_x(gstoreQueryModel.query_entity(entity_item))) > 0:
            printi("{} 该实体为真实体".format(entity_item))

        attr_list = gstoreQueryModel.parse_attribute(gstoreQueryModel.query_attribute(entity_item))

        ner_attr_dict[entity_item] = attr_list

    return ner_attr_dict


def choice_attribute(ner_attr_dict):
    for entity, attribute_list in ner_attr_dict:
        printi(entity)


def parse_classification(question):
    pass


def make_answer():
    pass


if __name__ == "__main__":
    question = ""
    el(question)
