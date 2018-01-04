#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/28 下午10:12
# @contact: zhouqiang847@gmail.com

import os

from importer import Imported
from robot import utils

IMPORTER = Imported()


class Namespace:
    """用来做变量和关键字的数据库，每一个实例对应一个测试套件"""

    def __init__(self, suite, parent, syslog):
        if suite is not None:
            syslog.info("Initializing namespace for test suite '%s'" % suite.name)
        self._syslog = syslog
        self.variables = _VariableScopes(suite, parent)
        self.suite = suite
        self._testlibs = {}
        # suite is None only when used internally by copy
        if suite is not None:
            self.import_library('BuiltIn')

    def import_library(self, name, args=None):
        """导入库，并保存到字典`_testlibs`中，例子:
        有个库:
            Class Collections:
                pass

        对应robot的导入语句如下:
        Library           Collections    WITH NAME    SL

        则key为`SL`，value为`PythonLibrary`实例

        对应robot的导入语句如下:
        Library           Collections

        则key为`Collections`，value为`PythonLibrary`实例

        """
        code_name, lib_name, args = self._get_lib_names_and_args(name, args)
        if self._testlibs.has_key(lib_name):
            self._syslog.warn("Test library '%s' already imported by suite '%s'"
                              % (lib_name, self.suite.longname))
            return
        lib = IMPORTER.import_library(code_name, args, self._syslog)
        if code_name != lib_name:
            lib = lib.copy(lib_name)
            self._syslog.info("Imported library '%s' with name '%s'"
                              % (code_name, lib_name))
        self._testlibs[lib_name] = lib
        lib.start_suite()
        # 为了动态导入
        # if self.test is not None:
        #     lib.start_test()

    def _get_lib_names_and_args(self, name, args):
        """返回一个元组，内容为(实际库名，自定义库名,参数列表)，如下:
        有个库:
            Class Collections:
                pass

        对应robot的导入语句如下:
        Library           Collections    WITH NAME    SL

        则实际库名为`Collections`，自定义库名为`SL`，参数列表为[]
        """
        if not os.path.exists(name):
            name = name.replace(' ', '')
        args = utils.to_list(args)
        if len(args) >= 2 and args[-2].upper() == 'WITH NAME':
            lib_name = args[-1].replace(' ', '')
            args = args[:-2]
        else:
            lib_name = name
        return name, lib_name, args


class _VariableScopes:
    """"""
    def __init__(self, suite, parent):
        if suite is not None:
            suite.variables.update(GLOBAL_VARIABLES)
            self._suite = self.current = suite.variables
        self._parents = []
        if parent is not None:
            self._parents.append(parent.namespace.variables.current)
            self._parents.extend(parent.namespace.variables._parents)
        self._test = None
        self._uk_handlers = []
