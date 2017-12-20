#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午12:43
@contact: zhouqiang847@gmail.com
"""
# 日志级别字典， NONE > ERROR > FAIL > WARN > DEBUG > TRACE
LEVELS = {
    "NONE": 100,
    "ERROR": 60,
    "FAIL": 50,
    "WARN": 40,
    "INFO": 30,
    "DEBUG": 20,
    "TRACE": 10,
}


def get_level(string):
    try:
        return LEVELS[string.upper()]
    except KeyError:
        raise Exception("Invalid log level '%s'" % string)
