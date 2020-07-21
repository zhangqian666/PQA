# -*-coding:utf-8 -*-

"""
version 0.1
    creator: yujy
    date: 2020/7/5
    comment: 实现 PoetrySchema 类，用于生成诗词图谱的 schema。
"""


import json
import re
import os.path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

import utils

# 类 label 不重复
__poetry_class__ = ('诗词', '朝代', '诗句', '人物', '地点', '状物', '体裁', '类别')

# 实体属性 label
__data_property__ = {'诗词': ('题名', '内容', '背景', '译文', '赏析'),
                     '朝代': ('朝代名', '朝代始', '朝代末'),
                     '诗句': ('内容', '译文'),
                     '人物': ('姓名', '别名', '生平简介', '轶事典故', '成就', '后世纪念', '出生年代'),
                     '地点': ('地点名', '曾用名'),
                     '状物': ('状物名', '寓意'),
                     '体裁': ('体裁名',),
                     '类别': ('类别名',)}
# (domain, range)
__object_property__ = {'作者': (('诗词', '人物'), ('诗句', '人物')),
                       '提到': (('诗词', '人物'), ('诗词', '地点'), ('诗词', '状物'), ('诗词', '朝代'),
                              ('诗句', '人物'), ('诗句', '地点'), ('诗句', '状物')),
                       '朝代': (('诗词', '朝代'), ('诗句', '朝代'), ('人物', '朝代')),
                       '类别': (('诗词', '类别'),),
                       '体裁': (('诗词', '体裁'),),
                       '属于': (('诗句', '诗词'),),
                       '上一句': (('诗句', '诗句'),),
                       '下一句': (('诗句', '诗句'),),
                       '祖籍': (('人物', '地点'),),
                       '出生地': (('人物', '地点'),)
                       }


class PoetrySchema(object):
    """
    生成或载入诗词图谱的schema
    """
    def __init__(self, schema=None, format=None):
        self.schema_graph = Graph()
        self.context = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "poetryc": "http://ictdba.apex.ac.cn/poetry/class/",
                        "poetryp": "http://ictdba.apex.ac.cn/poetry/property/",
                        "poetryr": "http://ictdba.apex.ac.cn/poetry/resource/"}
        self.__poetry_class = Namespace(self.context["poetryc"])
        self.__poetry_property = Namespace(self.context["poetryp"])

        self.all_classes = None
        self.all_properties = None
        self.__class_count = 0
        self.__property_count = 0

        self.build_schema(schema, format)

    def build_schema(self, schema=None, format=None):
        """
        构建 schema graph
        :param schema:
        :param format:
        :return:
        """
        if schema is None:
            self.schema_graph.namespace_manager.bind("poetryc", Namespace(self.context["poetryc"]))
            self.schema_graph.namespace_manager.bind("poetryp", Namespace(self.context["poetryp"]))
            self.schema_graph.namespace_manager.bind("poetryr", Namespace(self.context["poetryr"]))

            self.__class_count = 0
            self.__property_count = 0

            self.__create_class()
            self.__create_data_property()
            self.__create_object_property()
        else:
            self.schema_graph.parse(schema, format=format)
            self.__class_count, self.all_classes = self.__get_all_classes()
            self.__property_count, self.all_properties = self.__get_all_properties()

    def __create_class(self):
        """
        rdf:label 声明名称
        :return:
        """
        for c in __poetry_class__:
            cid = self.new_entity('class')
            self.schema_graph.add((cid, RDF.type, RDFS.Class))
            self.schema_graph.add((cid, RDFS.label, Literal(c, lang='zh')))

    def __create_data_property(self):
        """

            rdf:label 声明名称
        :return:
        """
        for key, value in __data_property__.items():
            cid = self.schema_graph.value(predicate=RDFS.label, object=Literal(key, lang='zh'))
            if cid is not None:
                for pv in value:
                    pid = self.new_entity('property')
                    self.schema_graph.add((pid, RDF.type, RDF.Property))
                    self.schema_graph.add((pid, RDFS.domain, cid))
                    self.schema_graph.add((pid, RDFS.range, XSD.string))
                    self.schema_graph.add((pid, RDFS.label, Literal(pv, lang='zh')))

    def __create_object_property(self):
        """

        :return:
        """
        for p_label, value in __object_property__.items():
            for v in value:
                pid = self.new_entity('property')
                # 添加 属性，label
                self.schema_graph.add((pid, RDF.type, RDF.Property))
                self.schema_graph.add((pid, RDFS.label, Literal(p_label, lang='zh')))
                # 添加 domain
                cid = self.get_class(v[0])
                self.schema_graph.add((pid, RDFS.domain, cid))
                # 添加 range
                cid = self.get_class(v[1])
                self.schema_graph.add((pid, RDFS.range, cid))

    def new_entity(self, entity):
        """
        生成class，使用
            C + ID (Integer) 表示class；
        生成实体属性，使用
            P + ID (Integer) 表示属性；
        :param entity:
        :return:
        """
        if not entity:
            return None

        if entity == 'class':
            self.__class_count += 1
            return self.__poetry_class["C" + str(self.__class_count)]
        elif entity == 'property':
            self.__property_count += 1
            return self.__poetry_property["P" + str(self.__property_count)]
        else:
            return None

    def get_class(self, label=None):
        """
        类的 label 唯一，不重复
        :param label:
        :return:
        """
        if label is None:
            return None
        qres = self.schema_graph.query(
            """ 
            select distinct ?x 
            where {
                ?x a rdfs:Class .
                ?x rdfs:label ?label .
            }
            order by ?x
            """, initBindings={"label": Literal(label, lang='zh')}
        )
        res = list(qres)
        if not res:
            return None
        else:
            return res[0][0]

    def get_data_property(self, poetry_class=None, label=None):
        """
        根据类和属性label，获取数据属性
        :param poetry_class:
        :param label:
        :return:
        """
        if poetry_class is None or label is None:
            return None

        if type(poetry_class) is str:
            # poetry_class 是类 label，则将其转成类
            poetry_class = self.get_class(poetry_class)

        qres = self.schema_graph.query(
            """ 
            select distinct ?x 
            where {
                ?x a rdf:Property .
                ?x rdfs:domain ?class .
                ?x rdfs:label ?label .
            }
            order by ?x
            """, initBindings={"class": poetry_class,
                               "label": Literal(label, lang='zh')}
        )
        res = list(qres)
        if not res:
            return None
        else:
            return res[0][0]

    def get_object_property(self, label=None, domain=None, range=None):
        """
        根据 domain 和 range，获取对象属性
        :param domain:
        :param range:
        :return:
        """
        if domain is None or range is None or label is None:
            return None

        if type(domain) is str:
            domain = self.get_class(domain)

        if type(range) is str:
            range = self.get_class(range)

        qres = self.schema_graph.query(
            """ 
            select distinct ?x 
            where {
                ?x a rdf:Property .
                ?x rdfs:domain ?domain .
                ?x rdfs:range ?range .
                ?x rdfs:label ?label .
            }
            order by ?x
            """, initBindings={"domain": domain,
                               "range": range,
                               "label": Literal(label, lang='zh')}
        )
        res = list(qres)
        if not res:
            return None
        else:
            return res[0][0]

    def __get_types(self, type=None):
        if not type:
            return None

        qres = self.schema_graph.query(
            """ 
            select distinct ?x
            where {
                ?x a ?type .
            }
            order by ?x
            """, initBindings={"type": type}
        )
        ret = [x for x in qres]
        return len(ret), ret

    def __get_all_classes(self):
        return self.__get_types(RDFS.Class)

    def __get_all_properties(self):
        return self.__get_types(RDF.Property)

    def schema2file(self, file, format):
        f = open(file, 'w')
        if format == 'json-ld':
            nt = str(self.schema_graph.serialize(format='json-ld', context=self.context, indent=4).decode('utf-8'))
        elif format == 'nt':
            nt = self.schema_graph.serialize(format='nt').decode('unicode-escape')
        elif format == 'turtle':
            nt = self.schema_graph.serialize(format='turtle').decode('utf-8')
        f.write(nt)
        f.close()


# 从清洗过的诗词数据生成RDF数据，暂时不用
class PoetryGraph(PoetrySchema):
    def __init__(self, schema=None, format=None):
        super(PoetryGraph, self).__init__(schema, format)
        self.poetry_graph = Graph() + self.schema_graph

        self.__poetry_resource = Namespace(self.context["poetryr"])
        self.__resource_count = 0

    def __get_resource_count(self):
        qres = self.schema_graph.query(
            """ 
            select distinct (count(*) as ?cnt) 
            where {
                ?x a ?o .
                filter(strstarts(str(?x), str(poetryr:)))
            } 
            order by ?x
            """
        )
        cnt = list(qres)
        if not cnt:
            return 0
        else:
            return cnt[0][0]

    def new_entity(self, entity):
        if not entity:
            return None
        if entity == 'class' or entity == 'property':
            return super().new_entity(entity)
        elif entity == 'resource':
            self.__resource_count += 1
            if self.__resource_count == 51949:
                self.__resource_count = 51949
            return self.__poetry_resource["R" + str(self.__resource_count)]
        else:
            return None

    def new_entity_resource(self):
        return self.new_entity('resource')

    def load_resources(self, file=None, format=None):
        ""
        if not file or not format:
            return None

        self.poetry_graph.parse(file, format)
        self.__class_count, self.all_classes = self.__get_all_classes()
        self.__property_count, self.all_properties = self.__get_all_properties()
        self.__resource_count = self.__get_resource_count()

    def get_resource(self, res_class=None, property=None, label=None):
        if not res_class or not label or not property:
            return None

        if type(res_class) is str:
            res_class = self.get_class(res_class)

        if type(property) is str:
            property = self.get_data_property(res_class, property)

        q = """
            select distinct ?r
            where {
                ?r ?p ?label
            } order by ?r
        """
        qres = self.poetry_graph.query(q, initBindings={"class": res_class,
                                                        "?p": property,
                                                        "label": Literal(label, lang='zh')})
        res = list(qres)
        if not res:
            return None
        else:
            return res[0][0]

    def load_neo4j_json(self, file=None):
        if not file:
            return None

        with open(file, 'r') as f:
            for line in f:
                data = json.loads(line)
                print(data)
                break

    def add_authors(self, dir=None, format=None):
        if dir is None:
            return None

        files = []
        if os.path.isdir(dir):
            files = utils.parse_filelist(dir, format)

        c = self.get_class('人物')
        name = self.get_data_property(c, '姓名')
        # brief = self.get_data_property(c, '生平简介')

        for file in files:
            # print(file, os.path.join(dir, file))
            with open(os.path.join(dir, file), 'r') as f:
                data = json.load(f)
                # print(data)
                for v in data:
                    rid = self.new_entity_resource()
                    self.poetry_graph.add((rid, RDF.type, c))
                    self.poetry_graph.add((rid, name, Literal(v['诗人姓名'], lang='zh')))
                    # self.poetry_graph.add((rid, brief, Literal(v['生平简介'], lang='zh')))

    def add_poetry(self, dir=None, format=None):
        """
        诗的信息，包括诗名、作者、诗的内容，利用这个可以添加诗句实体，
            以及诗和人物的关系、诗和诗句的关系、诗句和人物的关系、诗句和诗句的关系。
        :param dir:
        :param format:
        :return:
        """
        if dir is None:
            return None

        files = []
        if os.path.isdir(dir):
            files = utils.parse_filelist(dir, format)

        # 涉及的类
        poetry = self.get_class('诗词')
        verse_class = self.get_class('诗句')
        person = self.get_class('人物')

        # 涉及的属性
        title = self.get_data_property(poetry, '题名')
        poem_content = self.get_data_property(poetry, '内容')
        poem_author = self.get_object_property('作者', poetry, person)
        verse_author = self.get_object_property('作者', verse_class, person)
        verse_belongto_poem = self.get_object_property('属于', verse_class, poetry)
        next_verse = self.get_object_property('下一句', verse_class, verse_class)
        prev_verse = self.get_object_property('上一句', verse_class, verse_class)

        for file in files:
            # print(file, os.path.join(dir, file))
            with open(os.path.join(dir, file), 'r') as f:
                data = json.load(f)
                # print(data)
                for v in data:
                    poem = self.new_entity_resource()
                    # 添加 诗词 实体
                    self.poetry_graph.add((poem, RDF.type, poetry))
                    self.poetry_graph.add((poem, title, Literal(v['诗名'], lang='zh')))
                    self.poetry_graph.add((poem, poem_content, Literal(v['内容'], lang='zh')))
                    # 添加 诗词 与 人物 关系
                    personal = self.get_resource(person, '姓名', v['作者'])
                    if not personal:
                        personal = self.new_entity_resource()
                        self.poetry_graph.add((personal, RDF.type, person))
                        self.poetry_graph.add((personal, self.get_data_property(person, '姓名'), Literal(v['作者'], lang='zh')))
                    else:
                        self.poetry_graph.add((poem, poem_author, personal))
                    # 添加 诗句 实体以及 诗句与诗词 的关系
                    prev_v = None
                    for verse in re.split('，|。', v['内容']):
                        vres = self.new_entity_resource()
                        self.poetry_graph.add((vres, RDF.type, verse_class))
                        self.poetry_graph.add((vres, RDFS.label, Literal(verse, lang='zh')))

                        self.poetry_graph.add((vres, verse_author, personal))
                        self.poetry_graph.add((vres, verse_belongto_poem, poem))
                        if not prev_v:
                            prev_v = vres
                        else:
                            self.poetry_graph.add((prev_v, next_verse, vres))
                            self.poetry_graph.add((vres, prev_verse, prev_v))
                            prev_v = vres

    def graph2file(self, file=None, format=None):
        f = open(file, 'w')

        if format == 'json-ld':
            nt = str(self.poetry_graph.serialize(format='json-ld', context=self.context, indent=4).decode('utf-8'))
        elif format == 'nt':
            nt = self.poetry_graph.serialize(format='nt').decode('unicode-escape')
        elif format == 'turtle':
            nt = self.poetry_graph.serialize(format='turtle').decode('utf-8')
        f.write(nt)
        f.close()

    def test(self):
        data_dir = "./data/"
        self.load_neo4j_json(data_dir + 'all.json')


if __name__ == '__main__':
    # ps = PoetrySchema('./schema.json', 'json-ld')
    ps = PoetrySchema()
    # ps.test()
    # ps.build_schema()
    # ps.test()
    ps.schema2file('./data/schema.json', 'json-ld')
    # g = Graph()
    # g.parse('./schema.json', format='json-ld')

    # g = PoetryGraph('./data/schema.json', 'json-ld')
    # g.test()

