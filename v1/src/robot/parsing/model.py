#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午2:35
@contact: zhouqiang847@gmail.com
"""

from metadata import TestSuiteMetadata, TestCaseMetadata
from robot import utils
from rawdata import RawData
# from userkeyword import UserHandler
from keywords import KeywordList
from robot.errors import DataError


def TestSuiteData(datasources, settings, syslog):
    """"""
    if len(datasources) == 0:
        raise DataError("No Robot data sources given.")
    # elif len(datasources) > 1:
    #     return MultiSourceSuite(datasources, settings['SuiteNames'], syslog)
    # elif os.path.isdir(datasources[0]):
    #     return DirectorySuite(datasources[0], settings['SuiteNames'], syslog)
    # else:
    #     return FileSuite(datasources[0], syslog)
    return FileSuite(datasources[0], syslog)


class _BaseSuite:
    """测试套件基类"""

    def __init__(self, rawdata):
        name, source = self._get_name_and_source(rawdata.source)
        self.name = name
        self.source = source
        metadata = TestSuiteMetadata(rawdata)
        self.doc = metadata['Documentation']
        self.suite_setup = metadata['SuiteSetup']
        self.suite_teardown = metadata['SuiteTeardown']
        self.test_setup = metadata['TestSetup']
        self.test_teardown = metadata['TestTeardown']
        self.default_tags = metadata['DefaultTags']
        self.force_tags = metadata['ForceTags']
        self.test_timeout = metadata['TestTimeout']
        self.variables = rawdata.variables
        # self.user_keywords = UserHandler(rawdata.keywords)
        self.tests = None  # testcases

    def _get_name_and_source(self, path):
        """返回一个元祖(name, source)
        name:   表示测试套件名
        source: 表示测试套件所对应的文件路径
        """
        source = self._get_source(path)
        return self._get_name(source), source

    def _get_name(self, source):
        """返回测试套件名"""
        return utils.printable_name_from_path(source)


class FileSuite(_BaseSuite):
    """一个FileSuite实例表示一个测试套件，对应一个xx.tsv/xx.robot"""

    def __init__(self, path, syslog):
        syslog.info("Parsing test case file '%s'" % path)
        rawdata = self._get_rawdata(path, syslog)
        _BaseSuite.__init__(self, rawdata)
        self.tests = self._process_testcases(rawdata, syslog)

    def _get_rawdata(self, path, syslog):
        """获取文件内存模型"""
        rawdata = RawData(path, syslog)
        if rawdata.get_type() == rawdata.TESTCASE:
            return rawdata
        raise DataError("Test case file '%s' contains no test cases." % path)

    def _get_source(self, path):
        """返回文件路径"""
        return path

    def _process_testcases(self, rawdata, syslog):
        """循环遍历`rawdata.testcases`，每一个`rawtest`创建`TestCase`实例，并保存到列表中，最后返回该列表"""
        names = []
        tests = []
        for rawtest in rawdata.testcases:
            try:
                test = TestCase(rawtest)
            except:
                rawtest.report_invalid_syntax()
                continue
            tests.append(test)
            name = utils.normalize(test.name)
            if name in names:
                msg = "Multiple test cases with name '%s' in test suite '%s'"
                syslog.warn(msg % (test.name, self.name))
            else:
                names.append(name)
        return tests


class TestCase:
    def __init__(self, rawdata):
        self.name = utils.printable_name(rawdata.name)
        metadata = TestCaseMetadata(rawdata.metadata)
        self.doc = metadata['Documentation']
        self.tags = metadata['Tags']
        self.setup = metadata['Setup']
        self.teardown = metadata['Teardown']
        self.timeout = metadata['Timeout']
        self.keywords = KeywordList(rawdata.keywords)


# todo:最后删除掉
if __name__ == '__main__':
    from robot.output.systemLogger import SystemLogger

    TestSuiteData(['/Users/john/Desktop/robotframework-2.0/templates/testcase_template.tsv'], '', SystemLogger())
