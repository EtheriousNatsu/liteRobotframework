#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/29 下午4:42
# @contact: zhouqiang847@gmail.com

import sys
import inspect
from robot import utils


class _RunnableHandler:
    """XXXHandler基类"""
    type = 'library'

    def __init__(self, library, handler_name, handler_method):
        self.library = library
        self.doc = ''
        self.timeout = ''
        self.handler_name = handler_name
        self.name = handler_name
        self.longname = '%s.%s' % (library.name, self.name)
        self._method = library.scope == 'GLOBAL' and \
                       self._get_global_handler(handler_method, handler_name) or None

    def _get_global_handler(self, method, name):
        """"""
        return method


class PythonHandler(_RunnableHandler):
    """一个`PythonHandler`实例对应一个Python函数或类方法"""

    def __init__(self, library, handler_name, handler_method):
        _RunnableHandler.__init__(self, library, handler_name, handler_method)
        self.doc = utils.get_doc(handler_method)
        self.args, self.defaults, self.varargs \
            = self._get_arg_spec(handler_method)
        self.minargs = len(self.args) - len(self.defaults)
        self.maxargs = self.varargs is not None and sys.maxint or len(self.args)

    def _get_arg_spec(self, handler):
        """获取函数参数的名称和默认值，并返回`(args, defaults, varargs)`

        args     - 参数名
        defaults - 默认值
        varargs  - *args
        """
        args, varargs, kwargs, defaults = inspect.getargspec(handler)
        if inspect.ismethod(handler):
            args = args[1:]  # drop 'self'
        defaults = list(defaults) if defaults else []
        return args, defaults, varargs
