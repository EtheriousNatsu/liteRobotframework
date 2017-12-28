#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/18 上午3:39
@contact: zhouqiang847@gmail.com
"""


class BaseTestSuite(object):
    """测试套件基类"""

    def __init__(self, name='', source=None):
        self.name = name
        self.source = source
        self.suites = []
        self.tests = []
        self.setup = self.teardown = None


class BaseTestCase(object):
    """测试用例基类"""

    def __init__(self, name=''):
        self.name = name
        self.state = 'NOTRUN'
        self.critical = 'yes'
        self.setup = self.teardown = None
