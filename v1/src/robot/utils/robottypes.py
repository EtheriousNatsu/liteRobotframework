#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午7:30
@contact: zhouqiang847@gmail.com
"""
import types

_LIST_TYPES = [types.ListType, types.TupleType]


def is_str(item):
    """如果`item`的类型为`str`或`unicode`返回True，否则返回False"""
    return isinstance(item, basestring)


def is_list(item):
    """如果`item`的类型为`list`或`tuple`，返回True，否则False"""
    # TODO: Should support also other iterables incl. java.lang.Vector
    return type(item) in _LIST_TYPES


def to_list(item):
    """把item转为列表"""
    if item is None:
        return []
    if not is_list(item):
        raise Exception('Expected list, tuple or None')
    return list(item)


def unic(item):
    """把item转为unicode"""
    typ = type(item)
    if typ is types.UnicodeType:
        return item
    if typ is types.StringType:
        return item.decode('UTF-8', 'ignore')
    return unicode(item)
