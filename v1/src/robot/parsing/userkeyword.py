#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午3:23
@contact: zhouqiang847@gmail.com
"""
import sys

from robot import utils
from metadata import UserKeywordMetadata
from robot.variables import is_list_var, is_scalar_var
from keywords import KeywordList


class UserHandler():
    typr = 'user'

    def __init__(self, kwdata):
        self.name = utils.printable_name(kwdata.name)
        self.metadata = UserKeywordMetadata(kwdata.metadata)
        self.doc = self.metadata.get('Documentation', '')
        self.timeout = self.metadata.get('Timeout', [])
        self.keywords = KeywordList(kwdata.keywords)
        self.args, self.defaults, self.varargs \
            = self._get_arg_spec(self.metadata.get('Arguments', []))
        self.minargs = len(self.args) - len(self.defaults)
        self.maxargs = self.varargs is not None and sys.maxint or len(self.args)
        self.return_value = self.metadata.get('Return', [])

    def _get_arg_spec(self, origargs):
        """Returns argument spec in a tuple (args, defaults, varargs).

        args     - tuple of all accepted arguments
        defaults - tuple of default values
        varargs  - name of the argument accepting varargs or None

        Examples:
          ['${arg1}', '${arg2}']
            => ('${arg1}', '${arg2}'), (), None
          ['${arg1}', '${arg2}=default', '@{varargs}']
            => ('${arg1}', '${arg2}'), ('default',), '@{varargs}'
        """
        args = []
        defaults = []
        varargs = None
        for arg in origargs:
            if varargs is not None:
                # todo:异常处理
                raise Exception('Only last argument can be a list')
                # raise DataError('Only last argument can be a list')
            if is_list_var(arg):
                varargs = arg
                continue  # should be last round (otherwise DataError in next)
            if arg.count('=') == 0:
                default = None
            else:
                arg, default = arg.split('=', 1)
            if len(defaults) > 0 and default is None:
                # todo:异常处理
                raise Exception('Non default argument after default arguments')
                # raise DataError('Non default argument after default arguments')
            if not is_scalar_var(arg):
                # todo:异常处理
                raise Exception("Invalid argument '%s'" % arg)
                # raise DataError("Invalid argument '%s'" % arg)
            args.append(arg)
            if default is not None:
                defaults.append(default)
        return tuple(args), tuple(defaults), varargs
