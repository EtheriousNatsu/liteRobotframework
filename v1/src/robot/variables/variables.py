#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午3:36
@contact: zhouqiang847@gmail.com
"""

from robot import utils
from isvar import is_var
from robot.errors import DataError


class Variables(utils.NormalizedDict):
    """一个`Variables`实例代表测试套件中一组变量，如:
        *Variable*
        ${table_var}	foo
        @{table_listvar}	bar	${table_var}
        ${single_quoted}	s'ingle'qu'ot'es''
    """

    def __init__(self):
        utils.NormalizedDict.__init__(self, ignore=['_'])

    def set_from_variable_table(self, raw_variables):
        """遍历`raw_variables`,把变量填充到`Variables`实例中"""
        for rawvar in raw_variables:
            try:
                name, value = self._get_var_table_name_and_value(rawvar)
                if not self.data.has_key(name):
                    self.data[name] = value
            except:
                raise Exception("Setting variable failed")

    def _get_var_table_name_and_value(self, rawvar):
        """获取变量的`name`和`value`"""
        name = self._normalize(rawvar.name)
        if len(name) == 0:
            raise DataError('No variable name given')
        if name.endswith('=') and is_var(name[:-1]):
            name = name[:-1]
        elif not is_var(name):
            raise DataError("Invalid variable name '%s'" % rawvar.name)
        value = self._unescape_leading_trailing_spaces_from_var_table_value(rawvar.value)
        return name, value

    def _unescape_leading_trailing_spaces_from_var_table_value(self, value):
        """去掉`value`中的转义字符"""
        ret = []
        for item in value:
            if utils.is_str(item):
                if item.endswith(' \\'):
                    item = item[:-1]
                if item.startswith('\\ '):
                    item = item[1:]
            ret.append(item)
        return ret
