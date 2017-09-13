"""
sss
"""

import unittest
from robot.libraries.BuiltIn import BuiltIn


class _User1:
    def length(self):
        return 10


class _User2:
    def __init__(self):
        self.length = 20


class _User3:
    def __len__(self):
        return 30


class TestBuiltIn(unittest.TestCase):
    def setUp(self):
        self.builtIn = BuiltIn()

    def tearDown(self):
        self.builtIn = None

    def test_convert_to_boolean(self):
        assert self.builtIn.convert_to_boolean('true') == True
        assert self.builtIn.convert_to_boolean(0) == False

    def test_create_list(self):
        assert isinstance(self.builtIn.create_list(0, 1, 2), list)
        assert isinstance(self.builtIn.create_list([1, 2, 3]), list)
        assert isinstance(self.builtIn.create_list({'a':1, 'b':2}), list)

    def test_get_length(self):
        assert self.builtIn.get_length(_User1()) == 10
        assert self.builtIn.get_length(_User2()) == 20
        assert self.builtIn.get_length(_User3()) == 30

    def test_should_not_be_empty_fail(self):
        self.builtIn.should_not_be_empty('')

    def test_should_not_be_empty_success(self):
        self.builtIn.should_not_be_empty('123')

    def test_test_should_contain_success(self):
        self.builtIn.should_contain('abbbbb', 'ab')

    def test_should_contain_fail(self):
        self.builtIn.should_contain('abbbbb', 'c')

    def test_should_be_true_success(self):
        self.builtIn.should_be_true('1 > 0')

    def test_should_be_true_fail(self):
        self.builtIn.should_be_true('1 > 2')
