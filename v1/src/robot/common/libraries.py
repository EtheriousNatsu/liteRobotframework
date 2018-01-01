#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/29 上午11:00
# @contact: zhouqiang847@gmail.com

from robot.errors import DataError


class BaseLibrary:
    """"""

    def get_handler(self, name):
        """"""
        try:
            return self.handlers[name]
        except KeyError:
            raise DataError("No keyword handler with name '%s' found" % name)

    def has_handler(self, name):
        """"""
        return self.handlers.has_key(name)

    def __len__(self):
        return len(self.handlers)
