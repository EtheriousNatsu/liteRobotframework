#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/29 下午2:43
# @contact: zhouqiang847@gmail.com

import sys
import os


def norm_path(path):
    """标准化路径"""
    path = os.path.normpath(path)
    if os.sep == '\\':
        path = path.lower()
    return path


def add_paths(paths, to_beginning=False):
    """把`paths`添加到`sys.path`中"""
    for path in paths:
        add_path(path, to_beginning)


def add_path(path, to_beginning=False):
    """把`path`添加到`sys.path`中。
    如果`to_beginning`为True，则插入首位，否则插入末尾
    """
    path = norm_path(path)
    if path not in sys.path and os.path.exists(path):
        if to_beginning:
            sys.path.insert(0, path)
        else:
            sys.path.append(path)


def remove_path(path):
    """把`path`从`sys.path`中移除"""
    path = norm_path(path)
    while path in sys.path:
        sys.path.remove(path)


# 获取根目录
base = os.path.dirname(os.path.abspath(__file__))

# 把`/path/robot/..` 和 `/path/robot/libraries` 加入到`sys.path`并插入首位
paths = [os.path.join(base, p) for p in ['..', 'libraries']]
add_paths(paths, to_beginning=True)

# 删除根目录
remove_path(base)

# 把`PYTHONPATH`加入`sys.path`
try:
    add_paths(os.environ['PYTHONPATH'].split(os.pathsep))
except:
    pass

# 把当前目录加入`sys.path`
add_path('.')
