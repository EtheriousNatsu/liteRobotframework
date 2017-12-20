#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午3:44
@contact: zhouqiang847@gmail.com
"""

import sys


class CommandLineMonitor:
    def __init__(self, monitor_width=78):
        self._width = monitor_width
        self._started = False

    def start_suite(self, suite):
        """测试套件执行前打印测试套件名称。

        :param suite: 测试套件
        :return: None
        """
        if not self._started:
            self._write_separator('=')
        self._started = True
        self._write_info(suite.longname, suite.doc, start_suite=True)
        self._write_separator('=')

    def end_suite(self, suite):
        """测试套件结束后打印测试套件名称、状态及测试详情(如总共有多少个测试，成功了多少个，失败了多少个)"""

        self._write_info(suite.longname, suite.doc)
        self._write_status(suite.status)
        self._write_message(suite.get_full_message())
        self._write_separator('=')

    def start_test(self, test):
        """用例执行前打印用例名称。

        :param test: 测试用例
        :return: None
        """
        self._write_info(test.name, test.doc)

    def end_test(self, test):
        """
        用例结束后，打印用例状态。如果用例失败的话，还会打印失败信息。

        :param test: 测试用例
        :return:
        """
        self._write_status(test.status)
        self._write_message(test.message)
        self._write_separator('-')

    def _write_separator(self, sep_char):
        """打印分隔符"""
        self._write(self._width * sep_char)

    def _write_info(self, name, doc, start_suite=False):
        """
            1. 打印测试套件名称
            2. 打印测试用例名称
        """
        maxwidth = self._width
        if not start_suite:
            maxwidth -= len(' | PASS |')
        info = self._get_info(name, doc, maxwidth)
        self._write(info.ljust(maxwidth), newline=start_suite)

    def _get_info(self, name, doc, maxwidth):
        """
        1、如果 name 长度大于 maxwidth，则返回 '...' + name(截取)
        2、如果 doc 为空，直接返回name
        3、如果 info 长度大于 maxwidth，则返回 info(截取) + '...'

        """
        if len(name) > maxwidth:
            return '...' + name[-maxwidth + 3:]
        if doc == '':
            return name
        info = '%s :: %s' % (name, doc.splitlines()[0])
        if len(info) > maxwidth:
            info = info[:maxwidth - 3] + '...'
        return info

    def _write_status(self, status):
        """打印状态"""
        self._write(' | %s |' % status)

    def _write(self, msg, newline=True, stream=sys.stdout):
        """默认每次打印msg后，都会换行。"""
        if newline:
            msg += '\n'
        stream.write(msg)
        stream.flush()

    def error_message(self, message, level):
        """向stderr打印错误信息，给systemLogger使用"""
        message = '[ %s ] %s' % (level, message)
        self._write(message, stream=sys.stderr)

    def _write_message(self, message):
        """
            1. 测试套件执行后打印用例执行详细情况(如用例数多少、成功多少，失败多少)。
            2. 测试用例执行结束后，如果有异常信息，则打印异常信息。
        """
        if message:
            self._write(message.strip())
