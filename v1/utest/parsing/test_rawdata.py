#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/3 上午9:50
@contact: zhouqiang847@gmail.com
"""

import unittest
from robot.parsing.rawdata import TabularRawData

class _MockSyslog:
    pass


class TestTabularRawData(unittest.TestCase):
    def setUp(self):
        self.data = TabularRawData('/Users/john/Desktop/robotframework-2.0/templates/testcase_template.tsv', _MockSyslog())

    def test_start_setting_table(self):
        assert self.data.start_table('Setting')
        assert self.data._table._data is self.data.settings

    def test_start_variable_table(self):
        assert self.data.start_table('variable')
        assert self.data._table._data is self.data.variables

    def test_start_testcase_table(self):
        assert self.data.start_table('Test\tCase')
        assert self.data._table._data is self.data.testcases

    def test_invalid_table(self):
        for name in ['My Setting', 'Variablez', 'Test']:
            assert not self.data.start_table(name)

    def test_resource_type(self):
        self.data.start_table('Settings')
        self.data.add_row(['Name', 'Test'])
        self.assertEqual(self.data.get_type(), self.data.RESOURCE)
        self.data.start_table('Variables')
        self.data.add_row(['${var}', 'foo'])
        self.assertEquals(self.data.get_type(), self.data.RESOURCE)

    def test_testcase_type(self):
        self.data.start_table('Test Cases')
        self.data.add_row(['My test', 'Noop'])
        self.assertEquals(self.data.get_type(), self.data.TESTCASE)

if __name__ == '__main__':
    unittest.main()