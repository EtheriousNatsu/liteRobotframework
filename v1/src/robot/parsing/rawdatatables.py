#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/14 上午10:37
@contact: zhouqiang847@gmail.com
"""


class _Table:
    def __init__(self, name, source, data, syslog):
        self._name = name
        self.source = source
        self._data = data
        self._syslog = syslog

    def add_row(self, cells):
        if len(cells) == 0:
            return
        self._add_row(cells[0], cells[1:])

        # todo:异常处理
        # def report_invalid_syntax(self, row, error, level='ERROR'):
        #     msg = _ERR % (self._source, self._name, row, error)
        #     self._syslog.write(msg, level)


class SimpleTable(_Table):
    """"""
    def _add_row(self, name, value):
        item = SimpleItem(name, value, self)
        self._data.append(item)


class ComplexTable(_Table):
    def __init__(self, name, source, data, syslog):
        _Table.__init__(self, name, source, data, syslog)
        self._item = None

    def _add_row(self, name, data):
        if name != '':
            self._item = ComplexItem(name, self)
            self._data.append(self._item)
        if self._item is None:
            raise Exception("No name specified")
            # todo 异常处理
            # raise DataError('No name specified')
        self._item.add_subitem(data)


class _Item:
    def __init__(self, name, parent):
        self.name = name
        self._parent = parent

        # todo：异常处理
        # def report_invalid_syntax(self, error=None, level='ERROR'):
        #     if error is None:
        #         error = utils.get_error_message()
        #     self._parent.report_invalid_syntax(self._row, error, level)


class SimpleItem(_Item):
    def __init__(self, name, value, parrent):
        _Item.__init__(self, name, parrent)
        self.value = value


class ComplexItem(_Item):
    """Represents one item in Test Case or Keyword table"""

    def __init__(self, name, parrent):
        _Item.__init__(self, name, parrent)
        self.metadata = []
        self.keywords = []

    def add_subitem(self, data):
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
