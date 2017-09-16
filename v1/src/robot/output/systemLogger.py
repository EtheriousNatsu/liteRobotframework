#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午12:56
@contact: zhouqiang847@gmail.com
"""
from abstractLogger import AbstractLogger
from monitor import CommandLineMonitor


class SystemLogger(AbstractLogger):
    """"""

    def __init__(self, settings=None, monitor=None):
        AbstractLogger.__init__(self, "WARN")
        if monitor is None:
            self.monitor = CommandLineMonitor()
        else:
            self.monitor = monitor
            # try:
            #     self._file_logger = self._get_file_logger(settings['SyslogFile'],
            #                                               settings['SyslogLevel'])
            # except:
            #     self._file_logger = None
            #     self.error("Opening syslog file '%s' failed"
            #                % settings['SyslogFile'])

    def write(self, msg='', level='INFO'):
        # if self._file_logger is not None:
        #     self._file_logger.write(msg, level)
        AbstractLogger.write(self, msg, level)

    def _write(self, message):
        self.monitor.error_message(message.message, message.level)

    def _get_file_logger(self, path, level):
        if path == 'NONE':
            return None
        return _FileLogger(path, level)

    def close(self):
        if self._file_logger is not None:
            self._file_logger.close()
        self._file_logger = None


class _FileLogger(AbstractLogger):
    def __init__(self, path, level):
        AbstractLogger.__init__(level)
        self._write = self._get_write(path)

    def _get_write(self, path):
        return open(path, 'wb')

    def _write(self, message):
        entry = '%s | %s | %s\n' % (message.timestamp, message.level.ljust(5),
                                    message.message)
        self._write.write(entry)

    def close(self):
        self._write.close()


if __name__ == '__main__':
    syslog = SystemLogger()
    syslog.warn("Running test suite 'Testcase Template'")
    syslog.info('!!')
    syslog.set_level("INFO")
    syslog.info('!!')
