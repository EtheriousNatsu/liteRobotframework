#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午2:38
@contact: zhouqiang847@gmail.com
"""

from robot import utils


class _Metadata:
    """XXXMetadata基类"""

    def __init__(self, metadata=None):
        self._data = {}
        for name in self._names.values():
            self._data[name.replace(' ', '')] = None
        if metadata is not None:
            for item in metadata:
                self.set(item)

    def set(self, item):
        """根据`item`填充`self._data`"""
        try:
            name = self._names[utils.normalize(item.name)].replace(' ', '')
        except KeyError:
            raise Exception('Metadata init error')
            # todo:异常处理
            # self._report_invalid_meta(item)
        else:
            if self._data[name] is None:
                self._data[name] = item.value
            else:
                self._data[name].extend(item.value)

    def get(self, key, default=None):
        """根据key从self._data中取对应的value"""
        value = self._data[key]
        if value is None:
            return default
        if key == 'Documentation':
            return ' '.join(value)
        return value

    def __getitem__(self, key):
        return self.get(key)


class UserKeywordMetadata(_Metadata):
    _names = {'documentation': 'Documentation',
              'document': 'Documentation',
              'arguments': 'Arguments',
              'return': 'Return',
              'timeout': 'Timeout'}


class TestCaseMetadata(_Metadata):
    """测试用例元数据"""
    _names = {'documentation': 'Documentation',
              'document': 'Documentation',
              'setup': 'Setup',
              'precondition': 'Setup',
              'teardown': 'Teardown',
              'postcondition': 'Teardown',
              'tags': 'Tags',
              'timeout': 'Timeout'}


class TestSuiteMetadata(_Metadata):
    """测试套件元数据"""
    _names = {'documentation': 'Documentation',
              'document': 'Documentation',
              'suitesetup': 'Suite Setup',
              'suiteprecondition': 'Suite Setup',
              'suiteteardown': 'Suite Teardown',
              'suitepostcondition': 'Suite Teardown',
              'testsetup': 'Test Setup',
              'testprecondition': 'Test Setup',
              'testteardown': 'Test Teardown',
              'testpostcondition': 'Test Teardown',
              'defaulttags': 'Default Tags',
              'forcetags': 'Force Tags',
              'testtimeout': 'Test Timeout'}

    def __init__(self, rawdata=None):
        _Metadata.__init__(self)
        if rawdata is not None:
            self._set_rawdata(rawdata)

    def _set_rawdata(self, rawdata):
        """把`rowdata`中`settings`的数据填充到`TestSuiteMetadata`。如下:

           *** Settings ***
            Documentation     suite
            Force Tags        force tags
            Default Tags      default tags
            Test Timeout      10 seconds

            1、把每一行数据按`key=value`形式存到self._data中
        """
        for item in rawdata.settings:
            name = item.name.lower()
            if name in ['library', 'resource', 'variables']:
                pass
                # self.imports.append(ImportSetting(item))
            else:
                self.set(item)


# todo:为什么要写这个类出来，为什么要放在这里初始化呢？
class ImportSetting:
    def __init__(self, item):
        self._item = item
        self.name = item.name = utils.normalize(item.name).capitalize()
        self.value = None
