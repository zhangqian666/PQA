# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-19 11:25
"""
from EL.ner import *
from gstore_set.query_model import Model as GstoreModel


class RelationModel:

    def __init__(self):
        pass

    def UpAndDownSentences_simple_parse(self, question):
        entity_list = ner_on_work(question)
        print(entity_list)
        for label, entity in entity_list:
            print("{} {}".format(label, entity))
            if label.startswith("B-VER"):
                gstore_model = GstoreModel()

                true_entity_tag_list = gstore_model.query_entity(entity)
                print("根据{}查询到的实体的所有类型 ： {}".format(entity, true_entity_tag_list))

                true_entity_tag = disambiguation(question, entity, true_entity_tag_list)

                true_entity_uri = ""

                true_entity_tag_uri = ""

                true_entity_attr_list = []

                for true_entity_tag_item in true_entity_tag_list:
                    if true_entity_tag_item[0] == true_entity_tag:
                        true_entity_tag_uri = true_entity_tag_item[1]
                        true_entity_uri = true_entity_tag_item[2]
                        true_entity_attr_list = gstore_model.query_attribute(entity, true_entity_tag_uri)
                        print("查询到实体{} 的所有属性 ：  {}".format(label, true_entity_attr_list))

                true_entity_attr = disambiguation(question, entity, true_entity_attr_list)

                true_entity_attr_uri = ""

                for true_entity_attr_item in true_entity_attr_list:
                    if true_entity_attr_item[0] == true_entity_attr:
                        # 获取到主实体的所有的属性 ，进行属性消歧
                        true_entity_attr_uri = true_entity_attr_item[1]

                        answer = gstore_model.query_answer(true_entity_uri,
                                                           true_entity_attr_uri)
                        print("查询结果 ： {}".format(answer))

    def CottonWadOrder_simple_parse(self,question):

        entity_list = ltp_ner(question)
        print(entity_list)


    def FillInTheWords_simple_parse(self):
        pass

    def ErrorCorrection_simple_parse(self):
        pass

    def Disorder_simple_parse(self):
        pass

    def Other_simple_parse(self, question):
        entity_list = ner_on_work(question)
        print(entity_list)
        for label, entity in entity_list:
            print("{} {}".format(label, entity))
            if label.startswith("B"):
                gstore_model = GstoreModel()

                true_entity_tag_list = gstore_model.query_entity(entity)
                print("根据{}查询到的实体的所有类型 ： {}".format(entity, true_entity_tag_list))

                true_entity_tag = disambiguation(question, entity, true_entity_tag_list)

                true_entity_uri = ""

                true_entity_tag_uri = ""

                true_entity_attr_list = []

                for true_entity_tag_item in true_entity_tag_list:
                    if true_entity_tag_item[0] == true_entity_tag:
                        true_entity_tag_uri = true_entity_tag_item[1]
                        true_entity_uri = true_entity_tag_item[2]
                        true_entity_attr_list = gstore_model.query_attribute(entity, true_entity_tag_uri)
                        print("查询到实体{} 的所有属性 ：  {}".format(label, true_entity_attr_list))

                true_entity_attr = disambiguation(question, entity, true_entity_attr_list)

                true_entity_attr_uri = ""

                for true_entity_attr_item in true_entity_attr_list:
                    if true_entity_attr_item[0] == true_entity_attr:
                        # 获取到主实体的所有的属性 ，进行属性消歧
                        true_entity_attr_uri = true_entity_attr_item[1]

                        answer = gstore_model.query_answer_other_simple(true_entity_uri,
                                                                        true_entity_attr_uri)
                        print("查询结果 ： {}".format(answer))

    def TheMeaningOfWords_multi_parse(self):


        pass
