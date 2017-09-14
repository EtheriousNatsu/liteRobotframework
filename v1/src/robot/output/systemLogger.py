#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午12:56
@contact: zhouqiang847@gmail.com
"""
from abstractLogger import AbstractLogger


class SystemLogger(AbstractLogger):
    """"""


class _FileLogger(AbstractLogger):
    def __init__(self, path, level):
        AbstractLogger.__init__(level)
        self._write = self._get_write(path)

    def _get_write(self, path):
        return open(path, 'wb')

    def _write(self, message):
        entry = '%s | %s | %s\n' % (message.timestamp, message.level.ljust(5),
                                    message.message)
        self._write.write(entry)

    def close(self):
        self._write.close()
