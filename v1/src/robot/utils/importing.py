#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/16 下午5:21
@contact: zhouqiang847@gmail.com
"""
import os
import sys


def _split_path_to_module(path):
    """返回目录名及文件名(不包含后缀)"""
    moddir, modfile = os.path.split(path)
    modname = os.path.splitext(modfile)[0]
    return moddir, modname


def import_(name, type_='test library'):
    """
        1、 如果类名和模块名不同，则需要写成: myModule.myClass, 然后会在sys.path下找模块 myModule, 然后在 myModule 中找类 myClass。
        2、 如果类名和模块名相同，可以只提供类名 myClass。然后会在sys.path下找模块 myClass, 然后在 myClass 中找类 myClass。
        3、 如果 `name` 是一个包含模块的路径， 则首先把路径插入到 sys.path 中，然后按2走，导入成功后把路径从 sys.path 中删除。
    """
    if os.path.exists(name):
        moddir, name = _split_path_to_module(name)
        sys.path.insert(0, moddir)
        pop_sys_path = True
    else:
        pop_sys_path = False
    if name.count('.') > 0:
        parts = name.split('.')
        modname = '.'.join(parts[:-1])
        classname = parts[-1]
        fromlist = [str(classname)]
    else:
        modname = name
        classname = name
        fromlist = []
    try:
        module_or_class = __import__(modname, globals(), locals(), fromlist)
    except:
        if pop_sys_path:
            sys.path.pop(0)
            # _raise_import_failed(type_, name)
    if pop_sys_path:
        sys.path.pop(0)
    try:
        code = getattr(module_or_class, classname)
    except AttributeError:
        # if fromlist:
        #     _raise_no_lib_in_module(type_, modname, fromlist[0])
        code = module_or_class
    # if type(code) not in _VALID_IMPORT_TYPES:
    #     _raise_invalid_type(type_, code)
    return code
