# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 13:32
"""
from RE.relation_extraction import RelationModel
from classification.qa_classification import classif

poetry_type = [
    "UpAndDownSentences_simple",  # 上下句
    "CottonWadOrder_simple"  # 飞花令 描写某东西的诗词
    "FillInTheWords_simple",  # 填词
    "ErrorCorrection_simple",  # 错字
    "Disorder_simple",  # 乱序
    "Other_simple",  # 简单句
    "TheMeaningOfWords_multi"  # 词中意思
]


def handle_question(question):
    classification_result = classif(question)

    # 第二步 根据不同的问题用不同的处理方式
    # -》根据问题分类进行模型选择
    # -》实体识别 bert_ner
    # -》属性计算 consin
    # -》答案查询 rank

    print(classification_result)

    relation_model = RelationModel()

    entity = "问题类型为：{}；未查到正确结果。".format(classification_result)
    if classification_result is "Other_simple":
        entity = relation_model.Other_simple_parse(question)
    elif classification_result is "UpAndDownSentences_simple":
        entity = relation_model.UpAndDownSentences_simple_parse(question)

    # 第三步 构建答案 模版内容

    print(entity)
    # el(question)


if __name__ == "__main__":
    question = "千古名句“射人先射马，擒贼先擒王。”出自于哪位诗人之手？"
    # 第一步 问题分类 bert_classification
    handle_question(question)
