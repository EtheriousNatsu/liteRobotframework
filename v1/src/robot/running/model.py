#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午10:25
@contact: zhouqiang847@gmail.com
"""

from robot.variables import GLOBAL_VARIABLES
from robot import utils
from robot.parsing.model import TestSuiteData
from robot.common.model import BaseTestSuite
from robot.common.model import BaseTestCase
from robot.running.keywords import KeywordFactory


def TestSuite(datasources, settings, syslog):
    """生成可运行的测试套件"""
    suitedata = TestSuiteData(datasources, settings, syslog)
    suite = RunnableTestSuite(suitedata)
    return suite


class RunnableTestSuite(BaseTestSuite):
    """表示可运行的测试套件"""

    def __init__(self, suitedata, parentdatas=[]):
        parentdatas = parentdatas[:] + [suitedata]
        super(RunnableTestSuite, self).__init__(suitedata.name, suitedata.source)
        self.variables = GLOBAL_VARIABLES.copy()
        self.variables.set_from_variable_table(suitedata.variables)
        self.doc = suitedata.doc is not None and suitedata.doc or ''
        self.setup = utils.get_not_none(suitedata.suite_setup, [])
        self.teardown = utils.get_not_none(suitedata.suite_teardown, [])
        self.suites = [RunnableTestSuite(suite, parentdatas)
                       for suite in suitedata.suites]
        self.tests = [RunnableTestCase(test, parentdatas)
                      for test in suitedata.tests]


class RunnableTestCase(BaseTestCase):
    """表示可运行的测试用例"""

    def __init__(self, testdata, parentdatas):
        """初始化
            测试用例的setup会覆盖所属测试套件的test_setup
            测试用例的teardown会覆盖所属测试套件的test_teardown
            测试用例的timeout会覆盖所属测试套件的test_timeout
            测试用例的tags等于所属测试套件的force_tags + 测试用例自己的tags
        """
        BaseTestCase.__init__(self, testdata.name)
        self.doc = testdata.doc is not None and testdata.doc or ''
        test_setup, test_teardown, force_tags, default_tags, test_timeout \
            = self._proces_parents(parentdatas)
        self.setup = utils.get_not_none(testdata.setup, test_setup, [])
        self.teardown = utils.get_not_none(testdata.teardown, test_teardown, [])
        self.tags = force_tags + utils.get_not_none(testdata.tags, default_tags, [])
        self.timeout = utils.get_not_none(testdata.timeout, test_timeout, [])
        self.keywords = [KeywordFactory(kw) for kw in testdata.keywords]
        self.message = ''

    def _proces_parents(self, parentdatas):
        """获取所属测试套件的`test_setup`、`test_teardown`等属性"""
        test_setup = test_teardown = default_tags = test_timeout = None
        force_tags = []
        parentdatas.reverse()
        for parent in parentdatas:
            if parent.test_setup is not None and test_setup is None:
                test_setup = parent.test_setup
            if parent.test_teardown is not None and test_teardown is None:
                test_teardown = parent.test_teardown
            if parent.force_tags is not None:
                force_tags.extend(parent.force_tags)
            if parent.default_tags is not None and default_tags is None:
                default_tags = parent.default_tags
            if parent.test_timeout is not None and test_timeout is None:
                test_timeout = parent.test_timeout
        return test_setup, test_teardown, force_tags, default_tags, test_timeout


# todo:最后删除掉
if __name__ == '__main__':
    from robot.output.systemLogger import SystemLogger

    TestSuite(['/Users/john/Desktop/robotframework-2.0/templates/testcase_template.tsv'], '', SystemLogger())
