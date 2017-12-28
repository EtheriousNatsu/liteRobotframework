#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午3:26
@contact: zhouqiang847@gmail.com
"""
from robot import utils


class BaseKeyword:
    """一个BaseKeyword实例代表一个测试用例中一个关键字，如下:
        *Test Case*
        Failing	[Documentation]	FAIL Failing test case.
            Fail	Failing test case.  // 关键字
    """
    def __init__(self, name='', args=None, doc='', timeout='', type='kw'):
        self.name = name
        self.args = utils.to_list(args)
        self.doc = doc
        self.timeout = timeout
        self.type = type
