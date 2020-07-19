# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 13:32
"""
from EL.ner import ner_on_work
from gstore_set.query_model import Model as GstoreQueryModel
from utils.printUtil import *
from bert.run_classifier import *

poetry_type = [
    "UpAndDownSentences_simple",  # 上下句
    "CottonWadOrder_simple"  # 飞花令 描写某东西的诗词
    "FillInTheWords_simple",  # 填词
    "ErrorCorrection_simple",  # 错字
    "Disorder_simple",  # 乱序
    "Other_simple",  # 简单句
    "TheMeaningOfWords_multi"  # 词中意思
]


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
    """
    使用bert 分类器 对问题进行分类 在进行下面的计算
    :param question:
    :return:
    """
    pass


def make_answer():
    pass


if __name__ == "__main__":
    question = ""
    # 第一步 问题分类 bert_classification

    # 第二步 根据不同的问题用不同的处理方式
    # -》根据问题分类进行模型选择
    # -》实体识别 bert_ner
    # -》属性计算 consin
    # -》答案查询 rank

    # 第三步 构建答案 模版内容

    el(question)
