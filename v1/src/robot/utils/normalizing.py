#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午4:02
@contact: zhouqiang847@gmail.com
"""
import re, os
from UserDict import UserDict

_WHITESPACE_REGEXP = re.compile('\s+')
if os.sep == '\\':
    _CASE_INSENSITIVE_FILESYSTEM = True
else:
    try:
        _CASE_INSENSITIVE_FILESYSTEM = os.listdir('/tmp') == os.listdir('/TMP')
    except:
        _CASE_INSENSITIVE_FILESYSTEM = False


def normpath(path, normcase=True):
    """Returns path in normalized and absolute format.

    On case-insensitive file systems the path is also casenormalized
    (if normcase is True).
    """
    # if misc.is_url(path):
    #     return path
    # path = _absnorm(path)
    if normcase and _CASE_INSENSITIVE_FILESYSTEM:
        path = path.lower()
    # if os.sep == '\\' and len(path) == 2 and path[1] == ':':
    #     path += '\\'
    return path


def normalize(string, ignore=[], caseless=True, spaceless=True):
    """根据给定的规范规范string
       默认情况下，字符串变小写，所有空格被删除，
       在ignore列表中的多余字符会被删除。
    """
    if spaceless:
        string = _WHITESPACE_REGEXP.sub('', string)
    if caseless:
        string = string.lower()
        ignore = [ign.lower() for ign in ignore]
    for ign in ignore:
        string = string.replace(ign, '')
    return string


class NormalizedDict(UserDict):
    """自己实现的字典类"""

    def __init__(self, initial={}, ignore=[], caseless=True, spaceless=True):
        UserDict.__init__(self)
        self._ignore = ignore
        self._caseless = caseless
        self._spaceless = spaceless
        for key, value in initial.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.data[self._normalize(key)] = value

    set = __setitem__

    def __getitem__(self, key):
        return self.data[self._normalize(key)]

    def get(self, key, default=None):
        """根据key获取value，如果key不存在，返回None"""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def has_key(self, key):
        """如果key存在，返回True，否则False"""
        return self.data.has_key(self._normalize(key))

    __contains__ = has_key

    def _normalize(self, item):
        return normalize(item, self._ignore, self._caseless, self._spaceless)
