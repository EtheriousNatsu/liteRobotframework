#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/4 下午11:06
@contact: zhouqiang847@gmail.com
"""

import unittest
from robot.output.abstractLogger import AbstractLogger
import Selenium2Library

class TestAbstractLogger(unittest.TestCase):

    def test_set_threshold_invalid(self):
        logger = AbstractLogger('trace')
        self.assertRaises(Exception, logger.set_level, 'INVALID THRESHOLD')


    def test_getattr_with_invalid(self):
        logger = AbstractLogger('trace')
        try:
            logger.invalid('message')
            raise AssertionError, 'AttributeError not raised'
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()