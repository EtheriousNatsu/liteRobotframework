#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午9:27
@contact: zhouqiang847@gmail.com
"""

from robot.common.keyword import BaseKeyword


def KeywordList(rawkeywords):
    """遍历rawkeywords，生成一个关键字列表"""
    keywords = []
    for row in rawkeywords:
        kw = KeywordFactory(row)
        keywords.append(kw)
    return keywords


def KeywordFactory(kwdata):
    """初始化BaseKeyword实例"""
    return BaseKeyword(kwdata[0], kwdata[1:])
