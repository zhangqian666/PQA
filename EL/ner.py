# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:16
"""

import time
from bert_base.client import BertClient
from utils.printUtil import printi
import os
import jieba
from pyltp import Segmentor, Postagger, NamedEntityRecognizer
from bert_serving.client import BertClient as BertClient2
import numpy as np

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


def cos_sim(vector_a, vector_b):
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim


def disambiguation(question, entity, data_list):
    # ltp模型目录的路径
    LTP_DATA_DIR = '/home/admin/EA-CKGQA/nltp/ltp_data_v3.4.0'
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

    seg_list = list(jieba.cut(question))  # 分词处理，并且转化为列表形式
    wei_true_index = -1
    if seg_list.count(data_list) > 0:
        wei_true_index = seg_list.index(entity)

    print('seg_list为：', seg_list)  # 分词后的列表
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags_str = postagger.postag(seg_list)  # 对列表进行词性标注,并输出为str
    postags = list(postags_str)  # 转化为列表
    print(postags)  # 打印列表
    postagger.release()  # 释放模型

    keyword_list = keyword_chou(postags, 1, wei_true_index, seg_list)

    print('keywords_List为：', keyword_list)

    bc = BertClient2(port=5557, port_out=5558)

    candidate_attributes = data_list
    c = 0
    dict_attribute_score = {}

    for attribute in candidate_attributes:  # 候选属性
        #     scores_array = []
        for keyword in keyword_list:  # 关键词
            vector_attribute = bc.encode([attribute[0]])
            vector_keyword = bc.encode([keyword])

            c = cos_sim(vector_attribute, vector_keyword)
            # scores_array.append(c)
            dict_attribute_score[c] = attribute[0]
    #     scores_array = np.asarray(scores_array)np.mean(scores_array)

    keys = list(dict_attribute_score.keys())
    keys.sort(reverse=True)
    end_attribute = dict_attribute_score[keys[0]]
    print(end_attribute)
    return end_attribute


def keyword_chou(form_pos_list, form_entity_flag, form_wei_index, form_seg_list):
    """
    实体确认过后，再执行此函数才有效；
    执行效果为 把实体index除去，其余关键词均放入列表中，并进行return输出，供向量化替换使用
    :param form_seg_list:分词列表
    :param form_pos_list:词性列表
    :param form_entity_flag:实体是否锁定的标志位
    :param form_wei_index:上面函数return出来的临时保存索引号，此函数中对此索引号自动过滤掉
    :return:返回所有除去实体以外的关键词
    """
    pos_list = ["n", "nh", "ni", "nl", "ns", "nt", "nz", "ws", "v", "i", "r"]

    pos_list_count = 0  # 下方遍历计数使用

    keyword_list = []  # 创建关键词列表
    for if_named in form_pos_list:
        if form_entity_flag == 1:  # 锁定标志位必须被锁定，即 = 1，此函数才有效
            if pos_list_count != form_wei_index:  # 过滤
                if if_named in pos_list:
                    keyword_list.append(form_seg_list[pos_list_count])

        pos_list_count += 1
    return keyword_list
