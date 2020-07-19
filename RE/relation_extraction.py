# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-19 11:25
"""
from EL.ner import ner_on_work
from gstore_set.query_model import Model as GstoreModel


class RelationModel:

    def __init__(self):
        pass

    def UpAndDownSentences_simple_parse(self, question):
        entity_list = ner_on_work(question)
        print(entity_list)
        for label, entity in entity_list:
            if label is "B-VER":
                gstore_model = GstoreModel()
                attribute_list = gstore_model.query_attribute(entity)
                new_attribute_list = list(set(attribute_list))
                print("{} , {}".format(label, new_attribute_list))

    def CottonWadOrder_simple_parse(self):
        pass

    def FillInTheWords_simple_parse(self):
        pass

    def ErrorCorrection_simple_parse(self):
        pass

    def Disorder_simple_parse(self):
        pass

    def Other_simple_parse(self):
        pass

    def TheMeaningOfWords_multi_parse(self):
        pass
