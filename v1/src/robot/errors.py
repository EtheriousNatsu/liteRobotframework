#!/usr/bin/env python
# encoding: utf-8
# @version: 2.7
# @author: 'john'
# @time: 2017/12/20 上午10:59
# @contact: zhouqiang847@gmail.com


class RobotError(Exception):
    """异常基类"""


class DataError(RobotError):
    """当用户提供的测试数据不正确时，抛出该异常"""


class FrameworkError(RobotError):
    """当框架发生内部错误，抛出该异常"""
