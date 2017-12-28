#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午7:29
@contact: zhouqiang847@gmail.com
"""

from robot import utils


def is_var(string):
    """如果`string`为变量返回True，否则返回False"""
    if not utils.is_str(string):
        return False
    length = len(string)
    return length > 3 and string[0] in ['$', '@'] and string.rfind('{') == 1 \
           and string.find('}') == length - 1


def is_scalar_var(string):
    """如果`string`为变量且首字符为`$`，返回True，否则False"""
    return is_var(string) and string[0] == '$'


def is_list_var(string):
    """如果`string`为变量且首字符为`@`，返回True，否则False"""
    return is_var(string) and string[0] == '@'
