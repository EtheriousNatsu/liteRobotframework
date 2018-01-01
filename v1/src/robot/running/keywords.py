#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/28 下午5:52
# @contact: zhouqiang847@gmail.com


from robot.common.keyword import BaseKeyword


def KeywordFactory(kwdata):
    """根据`kwdata`的类型生产对应的运行时关键字"""
    if kwdata.type == 'kw':
        return Keyword(kwdata.name, kwdata.args)


class Keyword(BaseKeyword):
    """表示运行时的关键字,每个关键字拥有一个对应的handler"""

    def __init__(self, name, args, type='kw'):
        BaseKeyword.__init__(self, name, args, type=type)
        self.handler_name = name
