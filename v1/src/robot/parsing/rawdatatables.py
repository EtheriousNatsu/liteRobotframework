#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午11:06
@contact: zhouqiang847@gmail.com
"""


class _Table:
    def __init__(self, name, source, data, syslog):
        self._name = name
        self._source = source
        self._row = 0
        self._data = data
        self._syslog = syslog

    def add_row(self, cells, repeat=1):
        if len(cells) == 0:
            self._row += repeat
            return
        try:
            for i in range(repeat):
                self._row += 1
                self._add_row(cells[0], cells[1:])
        except:
            raise Exception()
            # self.report_invalid_syntax(self._row, utils.get_error_message())


class SimpleTable(_Table):
    def _add_row(self, name, value):
        if name == '...':
            try:
                self._data[-1].extend(value)
            except IndexError:
                raise Exception()
                # raise DataError('Invalid multirow usage: No item started')
        else:
            item = SimpleItem(name, value, self._row, self)
            self._data.append(item)


class ComplexTable(_Table):
    def __init__(self, name, source, data, syslog):
        _Table.__init__(self, name, source, data, syslog)
        self._item = None

    def _add_row(self, name, data):
        if name != '':
            self._item = ComplexItem(name, self._row, self)
            self._data.append(self._item)
        if self._item is None:
            raise Exception()
            # raise DataError('No name specified')
        self._item.add_subitem(data)


class _Item:
    def __init__(self, name, row, parent):
        self.name = name
        self._row = row
        self._parent = parent

    # def report_invalid_syntax(self, error=None, level='ERROR'):
    #     if error is None:
    #         pass
    #         error = utils.get_error_message()
    #     self._parent.report_invalid_syntax(self._row, error, level)


class ComplexItem(_Item):
    """Represents one item in Test Case or Keyword table"""

    def __init__(self, name, row, parent):
        _Item.__init__(self, name, row, parent)
        self.metadata = []
        self.keywords = []
        self._previous = None
        self._current_row = self._row - 1

    def add_subitem(self, data):
        self._current_row += 1
        if len(data) == 0:
            return
        name = data[0]
        if name == '...':
            pass
            # self._add_to_previous(data[1:])
        elif name == '' and len(data) > 1 and data[1] == '...':
            pass
            # self._add_to_previous(data[2:])
        elif name.startswith('[') and name.endswith(']'):
            name = name[1:-1].strip()   # removes '[' and ']'
            item = SimpleItem(name, data[1:], self._current_row, self._parent)
            self.metadata.append(item)
            self._previous = self.metadata
        else:
            self.keywords.append(data)
            self._previous = self.keywords

    def _add_to_previous(self, data):
        if self._previous is None:
            raise Exception()
            # raise DataError('Invalid multirow usage: No item started')
        self._previous[-1].extend(data)


class SimpleItem(_Item):
    def __init__(self, name, value, row, parent):
        _Item.__init__(self, name, row, parent)
        self.value = value

    def extend(self, value):
        self.value.extend(value)

    def copy(self):
        return SimpleItem(self.name, self.value[:], self._row, self._parent)