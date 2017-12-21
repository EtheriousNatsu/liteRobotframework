#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/14 上午10:22
@contact: zhouqiang847@gmail.com
"""

import re
import os
import urllib

from ..parsing.rawdatatables import SimpleTable, ComplexTable
from .. import utils
from TsvReader import TsvReader
from robot.errors import DataError

# Recognized table names
SETTING_TABLES = ['Setting', 'Settings', 'Metadata']
VARIABLE_TABLES = ['Variable', 'Variables']
TESTCASE_TABLES = ['Test Case', 'Test Cases']
KEYWORD_TABLES = ['Keyword', 'Keywords', 'User Keyword', 'User Keywords']
TABLE_NAMES = SETTING_TABLES + VARIABLE_TABLES + TESTCASE_TABLES + KEYWORD_TABLES

_WHITESPACE_REGEXP = re.compile('\s+')


def RawData(path, syslog, strip_comments=True):
    """读取文件内容，内存建模"""
    if path is None or os.path.isdir(path):
        return EmptyRawData(path)
    if utils.is_url(path):
        datafile = urllib.urlopen(path)
    else:
        datafile = open(path, 'rb')
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.html', '.xhtml', '.htm']:
        pass
    elif ext in ['.tsv']:
        reader = TsvReader()
    else:
        raise DataError("Unsupported file format '%s'" % ext)
    rawdata = TabularRawData(path, syslog, strip_comments)
    reader.read(datafile, rawdata)
    datafile.close()
    return rawdata


class _BaseRawData:
    """基类"""

    EMPTY = 1
    """No test data found"""
    RESOURCE = 2
    """Resource file i.e. variables and/or settings and/or keywords"""
    INITFILE = 3
    """Test suite init file -- same high level structure as in resource files"""
    TESTCASE = 4
    """Test case file i.e. test cases and optionally resources"""

    def __init__(self, source):
        self.source = source
        self.settings = []
        self.variables = []
        self.keywords = []
        self.testcases = []
        self._type = None

    def is_empty(self):
        return self.get_type() == self.EMPTY

    def get_type(self):
        if self._type is None:
            self._type = self._get_type()
        return self._type

    def _get_type(self):
        if len(self.testcases) > 0:
            return self.TESTCASE
        if len(self.settings) + len(self.variables) + len(self.keywords) == 0:
            return self.EMPTY
        if os.path.splitext(os.path.basename(self.source))[0].lower() == '__init__':
            return self.INITFILE
        return self.RESOURCE


class EmptyRawData(_BaseRawData):
    """如果文件不存在，则返回一个空的模型"""
    pass


class TabularRawData(_BaseRawData):
    """一个TabularRawData实例代表一个文件的内存模型"""

    def __init__(self, path, syslog):
        _BaseRawData.__init__(self, path)
        self._table = None
        self._syslog = syslog

    def start_table(self, name):
        """接收表格数据前的准备工作，比如
            *** Variables ***
            ${GREET}          Hello
            ${NAME}           world
            @{USER}           robot 123456
            &{USER2}          name=robot    password=secret

           在读取Variables表格数据前，初始化self._table=SimpleTable(*args)，并在实例化的过程中传self.variables。
           之后交由SimpleTable实例来读取Variables表格数据。
        """
        name = self._process_cell(name)
        table, data = self._get_table_and_data(name)
        if table is not None:
            self._table = table(name, self.source, data, self._syslog)
            return True
        else:
            self._table = None
            return False

    def _get_table_and_data(self, name):
        if utils.eq_any(name, SETTING_TABLES):
            return SimpleTable, self.settings
        if utils.eq_any(name, VARIABLE_TABLES):
            return SimpleTable, self.variables
        if utils.eq_any(name, TESTCASE_TABLES):
            return ComplexTable, self.testcases
        if utils.eq_any(name, KEYWORD_TABLES):
            return ComplexTable, self.keywords
        return None, None

    def add_row(self, cells):
        """添加row"""
        if self._table is not None:
            self._table.add_row(self._process_cells(cells))

    def _process_cells(self, cells):
        """"""
        temp = []
        for cell in cells:
            cell = self._process_cell(cell)
            temp.append(cell)
        for i in range(len(temp), 0, -1):
            if temp[i - 1] != '':
                break
            else:
                temp.pop()
        return temp

    def _process_cell(self, cell):
        """
            1、把cell中任意空白字符用' ' 代替
            2、移除cell头尾空格
        """
        return _WHITESPACE_REGEXP.sub(' ', cell).strip()
