#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/9/15 上午1:20
@contact: zhouqiang847@gmail.com
"""

import time


def get_time(format='timestamp', time_=None):
    """按要求的格式返回给定的或当前的时间。

    如果没有给出时间，则使用当前时间。返回的时间格式是基于`format`的。

    - 如果`format`包含`epoch`的话，则返回格林威治时间.
    - 如果`format`包含`year`,`month`,`day`,`hour`,`min`,`sec`，只返回选中部分。
    - 默认情况返回时间戳，如'2006-02-24 15:08:31'
    """
    if time_ is None:
        time_ = time.time()
    format = format.lower()
    # 1) 返回格林威治时间
    if format.count('epoch') > 0:
        return long(round(time_))
    timetuple = time.localtime(time_)
    parts = []
    for i, match in enumerate(['year', 'month', 'day', 'hour', 'min', 'sec']):
        if format.count(match) > 0:
            parts.append('%.2d' % timetuple[i])
    # 2) 返回时间戳
    if len(parts) == 0:
        return format_time(timetuple, daysep='-')
    # 返回选中部分
    elif len(parts) == 1:
        return parts[0]
    else:
        return parts


def format_time(timetuple, daysep='', daytimesep=' ', timesep=':', millissep=None):
    """把`time.localtime()`生成的时间元祖，按照给定的分隔符组装成一个字符串返回。"""
    daytimeparts = ['%02d' % t for t in timetuple[:6]]
    day = daysep.join(daytimeparts[:3])
    time_ = timesep.join(daytimeparts[3:6])
    return day + daytimesep + time_


def get_timestamp(daysep='', daytimesep=' ', timesep=':', millissep='.'):
    """返回当前格林威治时间戳"""
    timetuple = time.localtime()[:6]
    return format_time(timetuple, daysep, daytimesep, timesep, millissep)
