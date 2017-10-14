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
    str_ = normalize(str_, ignore, caseless, spaceless)
    for s in str_list:
        if str_ == normalize(s, ignore, caseless, spaceless):
            return True
    return False