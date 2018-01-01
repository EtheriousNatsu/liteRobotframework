#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/29 上午10:55
# @contact: zhouqiang847@gmail.com

from robot.running.testlibraries import TestLibrary
from robot import utils


class Imported:
    """"""

    def __init__(self):
        self._libraries = {}

    def import_library(self, name, args, syslog):
        """"""
        key = (name, tuple(args))
        if self._libraries.has_key(key):
            syslog.info("Found test library '%s' with args %s from cache"
                        % (name, utils.seq2str2(args)))
        else:
            lib = TestLibrary(name, args, syslog)
            self._libraries[key] = lib
            libtype = lib.__class__.__name__.replace('Library', '').lower()
            syslog.info("Imported library '%s' with args %s (%s type, %s scope, %d keywords)"
                        % (name, utils.seq2str2(args), libtype, lib.scope.lower(), len(lib)))
            if len(lib) == 0:
                syslog.warn("Imported library '%s' contains no keywords" % name)
        return self._libraries[key]
