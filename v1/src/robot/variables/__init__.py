#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午3:36
@contact: zhouqiang847@gmail.com
"""

from variables import Variables
import os
from robot import utils
from isvar import is_var, is_scalar_var, is_list_var


GLOBAL_VARIABLES = Variables()


# def init_global_variables(settings, syslog):
    # _set_cli_vars(settings, syslog)
    # for name, value in [ ('${TEMPDIR}', utils.get_temp_dir()),
    #                      ('${/}', os.sep),
    #                      ('${:}', os.pathsep),
    #                      ('${OUTPUTDIR}', settings['OutputDir']),
    #                      ('${OUTPUT_FILE}', settings['Output']),
    #                      ('${SUMMARY_FILE}', settings['Summary']),
    #                      ('${REPORT_FILE}', settings['Report']),
    #                      ('${LOG_FILE}', settings['Log']),
    #                      ('${DEBUG_FILE}', settings['DebugFile']),
    #                      ('${PREV_TEST_NAME}', ''),
    #                      ('${PREV_TEST_STATUS}', ''),
    #                      ('${PREV_TEST_MESSAGE}', ''),
    #                     ]:
    #     GLOBAL_VARIABLES[name] = value


# def _set_cli_vars(settings, syslog):
    # for varfile in settings['VariableFiles']:
    #     GLOBAL_VARIABLES.set_from_file(varfile, [], syslog)
    # for varstr in settings['Variables']:
    #     try:
    #         name, value = varstr.split(':', 1)
    #     except ValueError:
    #         name, value = varstr, ''
    #     GLOBAL_VARIABLES['${%s}' % name] = value
