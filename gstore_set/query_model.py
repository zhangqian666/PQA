# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:29
"""
from gstore_set.GstoreConnector import GstoreConnector
import json


class Model():

    def make_query(self, query_content):
        gstoreConnector = GstoreConnector("gstore9002.ngrok.apex.ac.cn", 6060, "root", "123456")
        return gstoreConnector.query("poetry", "json", query_content)

    def parse_json_x(self, json_str):
        print(json_str)
        all_part = json.loads(json_str)  # 读取所有文件内容
        end_ls = []
        try:
            results = all_part['results']  # 获取results标签下的内容
            results_bindings = results['bindings']  # 获取results标签下的bingdings内容
            # 定义一个list，将数据全部放到list中
            for res in results_bindings:
                res1 = res['x']
                res1 = res1['value']
                res2 = res["u"]
                res2 = res2["value"]
                if (res1, res2) not in end_ls:
                    end_ls.append((res1, res2))
        except:
            print("解析错误/或者数据为空")
        return end_ls

    def query_entity(self, entity):
        """
        查询实体 用于实体消歧
        :param entity:
        :return:
        """
        query1 = """
                  prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                  prefix poetryc: <http://ictdba.apex.ac.cn/poetry/class/>
                  prefix poetryp: <http://ictdba.apex.ac.cn/poetry/property/>
                  prefix poetryr: <http://ictdba.apex.ac.cn/poetry/resource/>

                  select distinct ?x ?u
                  where {
                     "%s"@zh ?u ?s. 
                     ?all_p a rdf:Property;
                          rdfs:label ?x;

                      FILTER(?u = ?all_p)
                  }
               """ % entity

        query2 = """
                  prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                  prefix poetryc: <http://ictdba.apex.ac.cn/poetry/class/>
                  prefix poetryp: <http://ictdba.apex.ac.cn/poetry/property/>
                  prefix poetryr: <http://ictdba.apex.ac.cn/poetry/resource/>
                  select distinct ?x ?u
                  where {
                      ?s ?u "%s"@zh. 
                      ?all_p a rdf:Property;
                          rdfs:label ?x;
                      FILTER(?u = ?all_p)
                  }
               """ % entity
        list1 = self.parse_json_x(self.make_query(query1))
        list2 = self.parse_json_x(self.make_query(query2))
        print(list1)
        list1.append(list2)
        return list1

    def query_attribute(self, entity, attr):
        """
                获取实体的所有属性
                :param entity:
                :return:

                """
        query1 = """
                  prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                  prefix poetryc: <http://ictdba.apex.ac.cn/poetry/class/>
                  prefix poetryp: <http://ictdba.apex.ac.cn/poetry/property/>
                  prefix poetryr: <http://ictdba.apex.ac.cn/poetry/resource/>
                   select distinct ?x ?u
                   where {
                      "%s"@zh <%s> ?s. 
                      ?s ?u ?o .
                      ?all_p a rdf:Property;
                          rdfs:label ?x;

                       FILTER(?u = ?all_p)
                   }
                """ % (entity, attr)

        query2 = """
                  prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix xsd: <http://www.w3.org/2001/XMLSchema#>
                  prefix poetryc: <http://ictdba.apex.ac.cn/poetry/class/>
                  prefix poetryp: <http://ictdba.apex.ac.cn/poetry/property/>
                  prefix poetryr: <http://ictdba.apex.ac.cn/poetry/resource/>
                   select distinct ?x ?u
                   where {
                      ?s <%s> "%s"@zh. 
                      ?s ?u ?o .
                      ?all_p a rdf:Property;
                          rdfs:label ?x;

                       FILTER(?u = ?all_p)
                   }
                """ % (attr, entity)
        list1 = self.parse_json_x(self.make_query(query1))
        list2 = self.parse_json_x(self.make_query(query2))
        print(list1)
        list1.append(list2)
        return list1

    def query_answer(self, entity, attribute):
        current_query = "SELECT ?x WHERE {<%s> <%s> ?x .}" % (entity, attribute)
        return current_query
