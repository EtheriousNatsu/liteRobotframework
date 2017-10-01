#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午10:41
@contact: zhouqiang847@gmail.com
"""
from tsvreader import TsvReader
import os, re
from robot import utils
from rawdatatables import SimpleTable, ComplexTable

# Hook for external tools for altering ${CURDIR} processing
PROCESS_CURDIR = True

# Recognized table names
SETTING_TABLES = ['Setting','Settings','Metadata']
VARIABLE_TABLES = ['Variable','Variables']
TESTCASE_TABLES = ['Test Case','Test Cases']
KEYWORD_TABLES = ['Keyword','Keywords','User Keyword','User Keywords']
TABLE_NAMES = SETTING_TABLES + VARIABLE_TABLES + TESTCASE_TABLES + KEYWORD_TABLES
_WHITESPACE_REGEXP = re.compile('\s+')


def RawData(path, syslog, strip_comments=True):
    try:
        datafile = open(path, 'rb')
    except:
        raise Exception()
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.tsv']:
        reader = TsvReader()
    else:
        raise Exception()
    rawdata = TabularRawData(path, syslog, strip_comments)
    reader.read(datafile, rawdata)
    datafile.close()
    return rawdata


class _BaseRawData:
    """Represents all unprocessed test data in one target file/directory."""

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


class TabularRawData(_BaseRawData):
    """Populates RawData from tabular test data"""

    def __init__(self, path, syslog, strip_comments=True):
        _BaseRawData.__init__(self, path)
        self._syslog = syslog
        self._table = None
        self._strip_comments = strip_comments
        # ${CURDIR} is replaced the data and thus must be escaped
        self._curdir = utils.get_directory(path).replace('\\', '\\\\')

    def start_table(self, name):
        """Makes rawdata instance ready to receive new data

        This method should be called with table's name before adding table's
        data with add_row.
        Returns False if data from specified table will not be processed. Client
        should thus check the return value of start_table and only call add_row
        if it receives True.
        """
        name = self._process_cell(name)
        table, data = self._get_table_and_data(name)
        if table is not None:
            self._table = table(name, self.source, data, self._syslog)
            return True
        else:
            self._table = None
            return False

    def add_row(self, cells, repeat=1):
        """Processes cells from given row.

        Client can use 'repeat' to tell that it has that many similar rows
        instead of calling add_row that many times.
        """
        if self._table is not None:
            self._table.add_row(self._process_cells(cells), repeat)


    def _process_cells(self, cells):
        """Trims cells and process ${CURDIR}.

        Trimming means collapsing whitespace, removing trailing empty cells and
        removing comments.
        """
        temp = []
        for cell in cells:
            # Remove leading and trailing whitespace and collapse internal
            cell = self._process_cell(cell)
            if self._strip_comments and cell.startswith('#'):
                break
            if PROCESS_CURDIR:
                cell = cell.replace('${CURDIR}', self._curdir)
            temp.append(cell)
        # Strip trailing empty cells
        for i in range(len(temp), 0, -1):
            if temp[i - 1] != '':
                break
            else:
                temp.pop()
        return temp

    def _get_table_and_data(self, name):
        if utils.eq_any(name, SETTING_TABLES):
            return SimpleTable, self.settings
        if utils.eq_any(name, VARIABLE_TABLES):
            return SimpleTable, self.variables
        if utils.eq_any(name, TESTCASE_TABLES):
            return ComplexTable, self.testcases
        # if utils.eq_any(name, KEYWORD_TABLES):
        #     return ComplexTable, self.keywords
        return None, None

    def _process_cell(self, cell):
        return _WHITESPACE_REGEXP.sub(' ', cell).strip()