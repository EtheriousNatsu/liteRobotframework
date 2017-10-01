#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午10:15
@contact: zhouqiang847@gmail.com
"""

from robot import utils
from robot.parsing import RawData

def TestSuiteData(datasources, setting, syslog):
    datasources = [utils.normpath(path)for path in datasources]
    if len(datasources) == 0:
        raise Exception()
    else:
        return FileSuite(datasources[0], syslog)




class FileSuite():
    def __init__(self, path, syslog):
        # syslog.info("Parsing test case file '%s'" % path)
        rawdata = self._get_rawdata(path, syslog)

    def _get_rawdata(self, path, syslog):
        rawdata = RawData(path, syslog)





