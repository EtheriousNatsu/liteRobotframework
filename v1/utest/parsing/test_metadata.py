#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/4 上午10:26
@contact: zhouqiang847@gmail.com
"""

import unittest
from robot.parsing.metadata import TestCaseMetadata, TestSuiteMetadata
from robot.utils.asserts import assert_equal
from robot import utils

tc_names = ('Documentation','Setup','Teardown','Tags')
suite_names = ('Documentation','TestSetup','TestTeardown','SuiteSetup',
               'SuiteTeardown','DefaultTags','ForceTags')


class _MockItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def extend(self, value):
        self.value.extend(value)

def _is_string_name(name):
    return utils.eq_any(name, ['Documentation'])

def test_set(meta, names):
    for name in names:
        if _is_string_name(name):
            test_set_string(meta, name)
        else:
            test_set_list(meta, name)


def test_set_string(meta, name):
    meta.set(_MockItem(name, ['hello']))
    assert_equal(meta.get(name), 'hello')
    meta.set(_MockItem(name, ['world']))
    assert_equal(meta.get(name), 'hello world')
    meta.set(_MockItem(name, ['and', 'hi', 'tellus']))
    assert_equal(meta.get(name), 'hello world and hi tellus')


def test_set_list(meta, name):
    meta.set(_MockItem(name, ['hello', 'again']))
    assert_equal(['hello', 'again'], meta.get(name))
    meta.set(_MockItem(name, ['world']))
    assert_equal(['hello', 'again', 'world'], meta.get(name))


class TestTestCaseMetadata(unittest.TestCase):

    def setUp(self):
        self.meta = TestCaseMetadata()

    def test_initial(self):
        for name in tc_names:
            self.assertEquals(self.meta.get(name), None)

    def test_set(self):
        test_set(self.meta, tc_names)



class TestTestSuiteMetadata(unittest.TestCase):

    def setUp(self):
        self.meta = TestSuiteMetadata()

    def test_initial(self):
        for name in suite_names:
            self.assertEquals(self.meta.get(name), None)

    def test_set(self):
        test_set(self.meta, suite_names)



if __name__ == '__main__':
    unittest.main()