#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/18 上午3:39
@contact: zhouqiang847@gmail.com
"""

from robot.common.statistics import Stat


class BaseTestSuite():
    """Base class for TestSuite used in runtime and by rebot."""

    def __init__(self, name='', source=None):
        self.name = name
        self.source = source
        self.metadata = {}
        self.suites = []
        self.tests = []
        self.critical_stats = Stat()
        self.all_stats = Stat()
        self.setup = self.teardown = None


class BaseTestCase(object):
    """测试用例基类"""

    def __init__(self, name=''):
        self.name = name
        self.state = 'NOTRUN'
        self.critical = 'yes'
        self.setUp = self.tearDown = None
