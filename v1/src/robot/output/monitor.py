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
        if not self._started:
            self._write_separator('=')
        self._started = True
        self._write_info(suite.longname, suite.doc, start_suite=True)
        self._write_separator('=')

    def end_suite(self, suite):
        self._write_info(suite.longname, suite.doc)
        self._write_status(suite.status)
        self._write_message(suite.get_full_message())
        self._write_separator('=')

    def start_test(self, test):
        self._write_info(test.name, test.doc)

    def end_test(self, test):
        self._write_status(test.status)
        self._write_message(test.message)
        self._write_separator('-')

    def _write_separator(self, str):
        self._write(self._width * str)

    def _write_info(self, name, doc, start_suite=False):
        maxwidth = self._width
        if not start_suite:
            maxwidth -= len(' | PASS |')
        info = self._get_info(name, doc, maxwidth)
        self._write(info.ljust(maxwidth), newline=start_suite)

    def _get_info(self, name, doc, maxwidth):
        if len(name) > maxwidth:
            return '...' + name[-maxwidth + 3:]
        if doc == '':
            return name
        info = '%s :: %s' % (name, doc.splitlines()[0])
        if len(info) > maxwidth:
            info = info[:maxwidth - 3] + '...'
        return info

    def _write_status(self, status):
        self._write(' | %s |' % status)

    def _write(self, msg, newline=True, stream=sys.stdout):
        if newline:
            msg += '\n'
        stream.write(msg)
        stream.flush()

    def error_message(self, message, level):
        message = '[ %s ] %s' % (level, message)
        self._write(message, stream=sys.stderr)

    def _write_message(self, message):
        self._write(message.strip())
