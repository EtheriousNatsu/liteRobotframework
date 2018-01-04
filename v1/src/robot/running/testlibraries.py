#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/29 上午10:58
# @contact: zhouqiang847@gmail.com

from types import ClassType, MethodType, FunctionType, ModuleType

from robot.common.libraries import BaseLibrary
from robot.output.systemLogger import SystemLogger
from robot import utils
from robot.running.handlers import PythonHandler
from robot.errors import DataError


def TestLibrary(name, args=None, syslog=None):
    """返回一个XXXLibrary实例"""
    if syslog is None:
        syslog = SystemLogger()
    libcode = utils.import_(name)
    args = utils.to_list(args)
    libtype = type(libcode)
    if libtype is ClassType:
        return PythonLibrary(libcode, name, args, syslog)
    if libtype is ModuleType:
        if args:
            raise DataError('Libraries implemented as modules do not take '
                            'arguments, got: %s' % str(args))
        return ModuleLibrary(libcode, name, args, syslog)


class _BaseTestLibrary(BaseLibrary):
    """XXXLibrary基类"""

    def __init__(self, libcode, name, args, syslog):
        """初始化，以一个类为例子:

            name: 类名
            args: 类初始化参数
            _instance_cache: 栈，用来暂存`_libinst`
            doc: 类描述
            scope: 类作用域
            _libcode: 类对象
            _libinst: 类实例
            handlers: `NormalizedDict`实例，以key=value形式保存类实例方法

        """
        self.name = name
        self.args = args
        self._instance_cache = []
        if libcode is not None:
            self.doc = utils.get_doc(libcode)
            self.scope = self._get_scope(libcode)
            self._libcode = libcode
            self._libinst = self.get_instance()
            self.handlers = self._create_handlers(syslog)
            self._init_scope_handling(self.scope)

    def _init_scope_handling(self, scope):
        """作用域初始化"""
        if scope == 'GLOBAL':
            return
        self._libinst = None
        self.start_suite = self._caching_start
        self.end_suite = self._restoring_end
        if scope == 'TESTCASE':
            self.start_test = self._caching_start
            self.end_test = self._restoring_end

    def _create_handlers(self, syslog):
        """返回一个`NormalizedDict`实例
        其中key为方法/函数名，value为`PythonHandler`实例
        """
        handlers = utils.NormalizedDict(ignore=['_'])
        for name in self._get_handler_names(self._libinst):
            err_pre = "Adding keyword '%s' to library '%s' failed: " % (name, self.name)
            try:
                method = self._get_handler_method(self._libinst, name)
                syslog.debug("Got handler method '%s'" % name)
            except TypeError:
                syslog.info(err_pre + 'Not a method or function')
                continue
            except:
                syslog.info(err_pre + 'Getting handler method failed')
                continue
            try:
                handlers[name] = self._create_handler(name, method)
                syslog.debug("Created keyword '%s'" % handlers[name].name)
            except:
                syslog.info(err_pre + 'Creating keyword failed')
        return handlers

    def _get_handler_names(self, libcode):
        """返回`libcode`的属性列表
        其中的`libcode`可以理解为类实例或模块。
        """
        return [name for name in dir(libcode)
                if not name.startswith('_') and name != 'ROBOT_LIBRARY_SCOPE']

    def _get_handler_method(self, libcode, name):
        """返回`libcode`的方法/函数
        其中`libcode`可以理解为类实例或模块
        """
        method = getattr(libcode, name)
        if type(method) not in [MethodType, FunctionType]:
            raise TypeError('Not a method or function')
        return method

    def get_instance(self):
        """赋值`_libinst`，并返回它
        其中的`_libinst`可以理解为类实例。
        """
        try:
            if self._libinst is None:
                self._libinst = self._get_instance()
        except AttributeError:
            self._libinst = self._get_instance()
        return self._libinst

    def _get_instance(self):
        """返回实例化的`_libcode`
        其中的`_libcode`可以理解为类对象。
        """
        try:
            return self._libcode(*self.args)
        except:
            self._raise_creating_instance_failed()

    def _get_scope(self, libcode):
        """返回`libcode`的作用域
        其中的`libcode`可以理解为类，作用域一般用`ROBOT_LIBRARY_SCOPE`命名。
        """
        try:
            scope = libcode.ROBOT_LIBRARY_SCOPE
            scope = utils.normalize(scope, ignore=['_']).upper()
        except:
            scope = 'TESTCASE'
        return scope in ['GLOBAL', 'TESTSUITE'] and scope or 'TESTCASE'

    def _raise_creating_instance_failed(self):
        """当创建类实例失败时，抛出`DataError`异常"""
        msg = "Creating an instance of the test library '%s' " % self.name
        if len(self.args) == 0:
            msg += "with no arguments "
        elif len(self.args) == 1:
            msg += "with argument '%s' " % self.args[0]
        else:
            msg += "with arguments %s " % utils.seq2str(self.args)
        msg += "failed"
        raise DataError(msg)

    def start_suite(self):
        pass

    def end_suite(self):
        pass

    def start_test(self):
        pass

    def end_test(self):
        pass

    def _caching_start(self):
        """把`_libinst`压入栈中，然后把`_libinst`设为None"""
        self._instance_cache.append(self._libinst)
        self._libinst = None

    def _restoring_end(self):
        """弹出栈中最新的一个元素，然后赋值给`_libinst`"""
        self._libinst = self._instance_cache.pop()

    def copy(self, name):
        """初始化一个`_BaseTestLibrary`实例，然后把当前XXLibrary实例的属性拷贝到它身上"""
        lib = _BaseTestLibrary(None, name, self.args, None)
        lib.doc = self.doc
        lib.scope = self.scope
        lib._libcode = self._libcode
        lib._libinst = self._libinst
        lib.handlers = utils.NormalizedDict(ignore=['_'])
        for name, handler in self.handlers.items():
            lib.handlers[name] = handler.copy(lib)
        return lib


class ModuleLibrary(_BaseTestLibrary):
    """一个`ModuleLibrary`实例对应一个实体模块"""

    def _get_scope(self, libcode):
        return 'GLOBAL'

    def get_instance(self):
        return self._libcode

    def _create_handler(self, handler_name, handler_method):
        """返回`PythonHandler`实例
        模块中的每个方法可以用一个`PythonHandler`实例表示。
        """
        return PythonHandler(self, handler_name, handler_method)


class PythonLibrary(_BaseTestLibrary):
    """一个`PythonLibrary`实例对应一个实体类"""

    def _create_handler(self, handler_name, handler_method):
        """返回`PythonHandler`实例
        类实例中每个方法可以用一个`PythonHandler`实例表示。
        """
        return PythonHandler(self, handler_name, handler_method)
