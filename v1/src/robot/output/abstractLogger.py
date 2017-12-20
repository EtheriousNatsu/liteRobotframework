#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午12:18
@contact: zhouqiang847@gmail.com
"""

from levels import get_level, LEVELS
from robot import utils


class AbstractLogger:
    """日志基类"""

    def __init__(self, level):
        self.set_level(level)

    def _is_logged(self, msg_level_str):
        msg_level = get_level(msg_level_str)
        return msg_level >= self.level

    def set_level(self, level_str):
        old = self._get_old_level()
        self.level = get_level(level_str)
        return old

    def _get_old_level(self):
        try:
            old_int = self.level
        except AttributeError:
            return None
        for level, int_value in LEVELS.items():
            if int_value == old_int:
                return level

    def write(self, msg='', level='INFO'):
        if self._is_logged(level):
            self._write(Message(msg, level))

    def _write(self, msg):
        raise NotImplementedError

    def trace(self, msg=''):
        self.write(msg, level='TRACE')

    def debug(self, msg=''):
        self.write(msg, level='DEBUG')

    def info(self, msg=''):
        self.write(msg, level='INFO')

    def warn(self, msg=''):
        self.write(msg, level='WARN')

    def fail(self, msg=''):
        self.write(msg, level='FAIL')

    def error(self, msg=''):
        self.write(msg, level='ERROR')


class Message:
    def __init__(self, message, level, html=False):
        self.timestamp = utils.get_timestamp(daysep='', daytimesep=' ',
                                             timesep=':', millissep='.')
        self.level = level.upper()
        self.message = message
