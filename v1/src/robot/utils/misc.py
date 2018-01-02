#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午12:44
@contact: zhouqiang847@gmail.com
"""

import os
import re
import tempfile

from robot.utils import unic
from robot.utils import is_str
from robot.utils import is_list


def get_doc(obj):
    """获取obj的说明"""
    try:
        doc = obj.__doc__
    except:
        doc = ''
    if doc is None or doc == '':
        return ''
    return '\n'.join([line.strip() for line in doc.strip().splitlines()])


_is_url_re = re.compile('^\w{2,}://')


def is_url(string):
    """判断是否是url"""
    return _is_url_re.search(string) is not None


def get_not_none(*args):
    """循环遍历args，返回第一个不为None的元素"""
    for arg in args:
        if arg is not None:
            return arg
    raise Exception('No non-None item found')


def get_directory(path):
    """Returns the directory part of the given path.

    If path already is a directory returns it as is, otherwise returns the
    directory containing the file
    """
    # if path.lower().startswith('http://'):
    #     return posixpath.dirname(path)
    # path = normpath(path)
    # if os.path.isdir(path):
    #     return path
    return os.path.dirname(path)


def printable_name_from_path(path):
    """从给定的路径(文件/目录)截取文件名，并返回它.

    例子:
        '/tmp/tests.py'         -> 'tests'
    """
    # 获取文件名/目录名，去掉前导路径和类型名称
    name = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
    return name


def get_temp_dir(extrapath=None):
    tempdir = tempfile.gettempdir()
    if not os.path.isdir(tempdir):
        raise EnvironmentError("Temp directory '%s' does not exist" % tempdir)
    if extrapath is not None:
        tempdir = os.path.join(tempdir, extrapath)
        # make sure there's no file with the same name as tempdir
        if os.path.isfile(tempdir):
            i = 1
            while os.path.isfile('%s%d' % (tempdir, i)):
                i += 1
            tempdir = '%s%d' % (tempdir, i)
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
    return tempdir


def seq2str(sequence, quote="'", sep=', ', lastsep=' and ', quote_all=False):
    """以'item 1', 'item 2' and 'item 3'格式返回一个序列"""

    def elem(string):
        if not is_str and not quote_all:
            return unic(string)
        return quote + unic(string) + quote

    if not is_list(sequence):
        return elem(sequence)
    elif len(sequence) == 0:
        return ''
    elif len(sequence) == 1:
        return elem(sequence[0])
    ret = []
    for i in range(len(sequence)):
        if i + 2 == len(sequence):
            ret.append(elem(sequence[i]) + lastsep + elem(sequence[i + 1]))
            break
        ret.append(elem(sequence[i]))
    return sep.join(ret)


def seq2str2(sequence):
    """以`[item1 | item2]`格式返回一个序列"""
    if not sequence:
        return '[ ]'
    return '[ %s ]' % ' | '.join([unic(item) for item in sequence])
