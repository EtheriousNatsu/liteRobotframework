#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/28 下午10:12
# @contact: zhouqiang847@gmail.com


class Namespace:
    """用来做变量和关键字的数据库，每一个实例对应一个测试套件"""

    def __init__(self, suite, parent, syslog):
        if suite is not None:
            syslog.info("Initializing namespace for test suite '%s'" % suite.name)
        self._syslog = syslog
        self.variables = _VariableScopes(suite, parent)
        self._testlibs = {}

    def import_library(self, name, args=None):
        """"""

    def _get_lib_names_and_args(self, name, args):
        """"""


class _VariableScopes:
    """"""
