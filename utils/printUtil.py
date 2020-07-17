# -*- coding: utf-8 -*-

"""
@author: zhangqian

@contact: 

@Created on: 2020-07-12 14:20
"""

isprint = True


def printi(str):
    if isprint:
        print(str)


def printe(str):
    if isprint:
        print("\033[32m {}".format(str))


def printw(str):
    if isprint:
        print("\033[31m {}".format(str))
