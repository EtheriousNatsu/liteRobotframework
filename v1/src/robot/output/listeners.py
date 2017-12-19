#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/16 上午4:37
@contact: zhouqiang847@gmail.com
"""

from robot import utils


class Listeners:
    def __init__(self, names, syslog):
        self._listeners = []
        for name in names:
            try:
                self._listeners.append(_Listener(name, syslog))
            except:
                syslog.error("Listeners error")

    def start_suite(self, suite):
        """测试套件开始前遍历 _listeners 里所有 listener实例执行start_suite()"""
        for listener in self._listeners:
            listener.start_suite(suite.name, suite.doc)

    def end_suite(self, suite):
        """测试套件结束后遍历 _listeners 里所有 listener实例执行end_suite()"""
        for listener in self._listeners:
            listener.end_suite(suite.status, suite.get_full_message())

    def start_test(self, test):
        """测试用例开始前遍历 _listeners 里所有 listener实例执行start_test()"""
        for listener in self._listeners:
            listener.start_test(test.name, test.doc, test.tags)

    def end_test(self, test):
        """测试结束后遍历 _listeners 里所有 listener实例执行end_test()"""
        for listener in self._listeners:
            listener.end_test(test.status, test.message)


class _Listener():
    def __init__(self, listener_name, syslog):
        """"""
        self._handlers = {}
        listener_class = utils.import_(listener_name, 'listener')
        listener = listener_class()
        for name in ['start_suite', 'end_suite', 'start_test', 'end_test',
                     'output_file', 'summary_file', 'report_file', 'log_file',
                     'debug_file', 'close']:
            self._handlers[name] = _Handler(listener, listener_name, name, syslog)

    def __getattr__(self, name):
        try:
            return self._handlers[name]
        except KeyError:
            raise AttributeError


class _Handler:
    def __init__(self, listener, listener_name, name, syslog):
        self._handler, self._name = self._get_handler(listener, name)
        self._listener_name = listener_name
        self._syslog = syslog

    def __call__(self, *args):
        try:
            self._handler(*args)
        except:
            self._syslog.error("Calling '%s' method of listener '%s' failed: %s")
            self._syslog.info("Details:\n%s")

    def _get_handler(self, listener, name):
        try:
            try:
                return getattr(listener, name), name
            except AttributeError:
                name = self._toCamelCase(name)
                return getattr(listener, name), name
        except AttributeError:
            return lambda *args: None, None

    def _toCamelCase(self, name):
        parts = name.split('_')
        return ''.join([parts[0]] + [part.capitalize() for part in parts[1:]])
