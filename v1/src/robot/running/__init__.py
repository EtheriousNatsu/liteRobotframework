#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/28 下午5:56
# @contact: zhouqiang847@gmail.com


class _Namespaces:
    """用来保存当前suite的Namespace实例，供外部使用
    其中的`_namespaces`保存当前suite的上一个suite的Namespace实例
    """

    def __init__(self):
        self._namespaces = []
        self.current = None

    def start_suite(self, namespace):
        self._namespaces.append(self.current)
        self.current = namespace

    def end_suite(self):
        self.current = self._namespaces.pop()


NAMESPACES = _Namespaces()
