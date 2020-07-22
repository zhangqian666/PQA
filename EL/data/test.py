# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-17 14:54
"""

# with open("/Users/zhangqian/PycharmProjects/PQA/EL/data/poetry_origin.txt" ,"r",encoding="utf-8") as f:
#     with open("/Users/zhangqian/PycharmProjects/PQA/EL/data/poetry_origin2.txt","w",encoding="utf-8") as f2:
#         for line in f.readlines():
#             if line == "\n":
#                 line = ""
#             f2.write(line)

with open("/Users/zhangqian/PycharmProjects/PQA/EL/data/poetry_origin2.txt", "r", encoding="utf-8") as f:
    with open("/Users/zhangqian/PycharmProjects/PQA/EL/data/poetry_data3.txt", "w", encoding="utf-8") as f2:
        i = 0
        j = 0
        for line in f.readlines():
            if line == "\n":
                line = ""
            if i % 2 == 0:
                f2.write("{} {}".format(j, line))
                j += 1
            else:
                pass
                # f2.write(line)
            i += 1
