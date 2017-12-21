#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/14 上午10:37
@contact: zhouqiang847@gmail.com
"""

from robot.errors import DataError


class _Table:
    """table基类"""

    def __init__(self, name, source, data, syslog):
        self._name = name
        self.source = source
        self._data = data
        self._syslog = syslog

    def add_row(self, cells):
        """添加行数据，底层由子类实现"""
        if len(cells) == 0:
            return
        self._add_row(cells[0], cells[1:])


class SimpleTable(_Table):
    """一个SimpleTable实例代表一个表格(如variables/settings)"""

    def _add_row(self, name, value):
        """初始化一个SimpleItem实例代表表格中一行数据，并保存到self._data中"""
        item = SimpleItem(name, value, self)
        self._data.append(item)


class ComplexTable(_Table):
    """一个ComplexTable实例代表一个表格(如testcases/keywords)"""

    def __init__(self, name, source, data, syslog):
        _Table.__init__(self, name, source, data, syslog)
        self._item = None

    def _add_row(self, name, data):
        """"""
        if name != '':
            self._item = ComplexItem(name, self)
            self._data.append(self._item)
        if self._item is None:
            raise DataError('No name specified')
        self._item.add_subitem(data)


class _Item:
    """xxxItem基类"""

    def __init__(self, name, parent):
        self.name = name
        self._parent = parent


class SimpleItem(_Item):
    """SimpleItem映射一行数据"""

    def __init__(self, name, value, parrent):
        _Item.__init__(self, name, parrent)
        self.value = value


class ComplexItem(_Item):
    """"""

    def __init__(self, name, parrent):
        _Item.__init__(self, name, parrent)
        self.metadata = []
        self.keywords = []

    def add_subitem(self, data):
        """"""
        if len(data) == 0:
            return
        name = data[0]
        if name.startswith('[') and name.endswith(']'):
            name = name[1:-1].strip()  # removes '[' and ']'
            item = SimpleItem(name, data[1:], self._parent)
            self.metadata.append(item)
            self._previous = self.metadata
        else:
            self.keywords.append(data)
