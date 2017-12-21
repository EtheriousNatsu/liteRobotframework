#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午11:25
@contact: zhouqiang847@gmail.com
"""
from normalizing import normalize


def eq_any(str_, str_list, ignore=[], caseless=True, spaceless=True):
    """遍历str_list，只要其中有一个元素与str_相等，返回True"""
    str_ = normalize(str_, ignore, caseless, spaceless)
    for s in str_list:
        if str_ == normalize(s, ignore, caseless, spaceless):
            return True
    return False
