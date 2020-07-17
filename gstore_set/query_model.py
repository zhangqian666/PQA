# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:29
"""
from gstore_set.GstoreConnector import GstoreConnector
import json


class Model():
    current_query = ""

    def make_query(self):
        gstoreConnector = GstoreConnector("gstore.ngrok.apex.ac.cn", 6060, "root", "123456")
        return gstoreConnector.query("pg", "json", self.current_query)

    def parse_json_x(self, json_str):
        all_part = json.loads(json_str)  # 读取所有文件内容
        results = all_part['results']  # 获取results标签下的内容
        results_bindings = results['bindings']  # 获取results标签下的bingdings内容
        # 定义一个list，将数据全部放到list中
        end_ls = []
        for res in results_bindings:
            res1 = res['x']
            res1 = res1['value']
            if res1 not in end_ls:
                end_ls.append(res1)
        return end_ls

    def query_entity(self, entity):
        """
        获取实体的所有属性
        :param entity:
        :return:
        """
        self.current_query = "SELECT ?x WHERE {<%s> ?x ?y .}" % entity
        return self.make_query()

    def query_attribute(self, entity):
        """
        获取实体的所有属性
        :param entity:
        :return:
        """
        self.current_query = "SELECT ?x WHERE {<%s> ?x ?y .}" % entity

        return self.make_query()

    def parse_attribute(self, query_result):
        """
        获取到实体的所有属性 去重
        :param query_result:
        :return:
        """
        attribute_list = self.parse_json_x(query_result)
        return list(set(attribute_list))

    def query_answer(self, entity, attribute):
        current_query = "SELECT ?x WHERE {<%s> <%s> ?x .}" % (entity, attribute)
        return current_query
