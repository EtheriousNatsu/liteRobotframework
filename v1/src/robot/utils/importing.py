#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/16 下午5:21
@contact: zhouqiang847@gmail.com
"""
import os, sys


def _split_path_to_module(path):
    moddir, modfile = os.path.split(path)
    modname = os.path.splitext(modfile)[0]
    return moddir, modname

def import_(name, type_='test library'):
    """Imports Python class/module or Java class with given name.

        'name' can also be a path to the library and in that case the directory
        containing the lib is automatically put into sys.path and removed there
        afterwards.

        'type_' is used in error message if importing fails.

        Class can either live in a module/package or be 'standalone'. In the former
        case tha name is something like 'MyClass' and in the latter it could be
        'your.package.YourLibrary'). Python classes always live in a module but if
        the module name is exactly same as the class name the former also works in
        Python.

        Example: If you have a Python class 'MyLibrary' in a module 'mymodule'
        it must be imported with name 'mymodule.MyLibrary'. If the name of
        the module is also 'MyLibrary' then it is possible to use only
        name 'MyLibrary'.
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
