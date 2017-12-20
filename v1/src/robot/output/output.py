#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午12:28
@contact: zhouqiang847@gmail.com
"""

from abstractLogger import AbstractLogger
from monitor import CommandLineMonitor
from systemLogger import SystemLogger
from listeners import Listeners


class Output(AbstractLogger):
    """"""

    def __init__(self, settings):
        AbstractLogger.__init__(self, "WARN")
        self.monitor = CommandLineMonitor()
        self.syslog = SystemLogger(settings, self.monitor)
        self.listeners = Listeners(settings['Listeners'], self.syslog)
        self._settings = settings

    def start_suite(self, suite):
        self.syslog.info("Running test suite '%s'" % suite.longname)
        self.monitor.start_suite(suite)
        self.listeners.start_suite(suite)

    def end_suite(self, suite):
        self.monitor.end_suite(suite)
        self.listeners.end_suite(suite)

    def start_test(self, test):
        self.syslog.info("Running test case '%s'" % test.name)
        self.monitor.start_test(test)
        self.listeners.start_test(test)

    def end_test(self, test):
        self.monitor.end_test(test)
        self.listeners.end_test(test)


# ####################
# test case
#########################
class _Suite():
    def __init__(self):
        self.longname = self.name = 'Testcase Template'
        self.doc = 'A complex testdata file in tsv format.'
        self.status = 'pass'

    def get_full_message(self):
        return "1 critical tests, 1 passed, 0 failed \n" \
               "1 tests total, 1 passed, 0 failed"


class _Test():
    def __init__(self):
        self.name = 'Failing'
        self.doc = 'FAIL Failing test case'
        self.status = 'pass'
        self.message = 'Failing test case.'
        self.tags = ''


if __name__ == '__main__':
    suite = _Suite()
    test = _Test()
    dic = {"Listeners": ["/Users/john/Desktop/robotframework-2.0/templates/BitteWartenMitArg.py"]}
    output = Output(settings=dic)
    output.start_suite(suite)
    output.start_test(test)
    output.end_test(test)
    output.end_suite(suite)
