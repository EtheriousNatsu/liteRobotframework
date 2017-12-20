#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/12/20 上午10:53
@contact: zhouqiang847@gmail.com
"""

from robot.errors import DataError
from robot import output


class _Converter:
    def convert_to_integer(self, item):
        """把item转成integer类型"""
        try:
            return long(item)
        except:
            raise DataError("%s cannot be converted to an integer" % item)

    def convert_to_number(self, item):
        """把item转为float类型"""
        try:
            return float(item)
        except:
            raise DataError("%s cannot be converted to a floating ponit number" % item)

    def create_list(self, *items):
        """创建一个列表"""
        return list(items)


class _Verify:
    def get_length(self, item):
        """返回item的长度。
            1、首先调用item的__len__方法
            2、再尝试调用item的length()方法
            3、再尝试调用item的length属性
        """
        try:
            return len(item)
        except:
            pass
        try:
            return item.length()
        except:
            pass
        try:
            return item.length
        except:
            raise Exception("Could not get length of '%s" % item)

    def should_be_true(self, expr, msg=None):
        """如果eval(expr)为False，则抛出AssertionError异常。
        """
        if msg is None:
            msg = "%s should be true" % expr
        if not isinstance(expr, basestring):
            raise Exception("%s should be str" % expr)
        if not bool(eval(expr)):
            raise AssertionError(msg)

    def should_contain(self, str1, str2, msg=None):
        """如果str1不包括str2，则抛出AssertionError。"""
        msg = self._get_string_msg(str1, str2, msg, "does not contain")
        if str1.count(str2) < 1:
            raise AssertionError(msg)

    def should_not_be_empty(self, item, msg=None):
        """判断item是否为空，如果item长度为0，则抛出AssertionError."""
        if self.get_length(item) == 0:
            if msg is None:
                msg = "%s should not be empty" % item
            raise AssertionError(msg)

    def _get_string_msg(self, str1, str2, msg, delim):
        """返回一个组装好的(根据delim组装)msg，(e.g. 1 ！= 2)"""
        _msg = "%s %s %s" % (str1, delim, str2)
        if msg is None:
            msg = _msg
        return msg


class _Misc:
    def evaluate(self, expression):
        """计算expression的值，并返回。
        """
        try:
            return eval(expression)
        except:
            raise

    def catenate(self, *items):
        """把items按照分隔符连接起来，并返回结果字符串。
            1、如果没指定分隔符，默认为空格。
            2、通过 SEPARATOR=x，来指定分隔符。
        """
        if len(items) == 0:
            return u''
        if items[0].startswith('SEPARATOR='):
            sep = items[0][len('SEPARATOR='):]
            items = items[1:]
        else:
            sep = u' '
        return sep.join(items)

    def log(self, message, level="INFO"):
        """打印message"""
        level = level.upper()
        if not output.LEVELS.has_key(level):
            raise DataError("Invalid log level '%s'" % level)
        print '*%s* %s' % (level, message)

    def log_many(self, *messages):
        """打印多条message"""
        for message in messages:
            self.log(message)


class BuiltIn(_Converter, _Verify, _Misc):
    """对外暴露的内置库"""
    pass
