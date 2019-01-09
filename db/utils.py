# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: utils.py 
@time: 2018/12/30
@contact: limuyu0110@pku.edu.cn

"""
from db.config import *


def check(key_list, can_dict, task):
    for key in key_list:
        if key not in can_dict:
            logging.debug(F'key:{key}, not in given data, in task {task}!!! Exit...')
            return 0
    return 1


def judge_similar(s1, s2):
    for c in s1:
        if c not in s2:
            return 0
    return 1
