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
    """Return the given or current time in requested format.

    If time is not given, current time is used. How time is returned is
    is deternined based on the given 'format' string as follows. Note that all
    checks are case insensitive.

    - If 'format' contains word 'epoch' the time is returned in seconds after
      the unix epoch.
    - If 'format' contains any of the words 'year', 'month', 'day', 'hour',
      'min' or 'sec' only selected parts are returned. The order of the returned
      parts is always the one in previous sentence and order of words in
      'format' is not significant. Parts are returned as zero padded strings
      (e.g. May -> '05').
    - Otherwise (and by default) the time is returned as a timestamp string in
      format '2006-02-24 15:08:31'
    """
    if time_ is None:
        time_ = time.time()
    format = format.lower()
    # 1) Return time in seconds since epoc
    if format.count('epoch') > 0:
        return long(round(time_))
    timetuple = time.localtime(time_)
    parts = []
    for i, match in enumerate(['year', 'month', 'day', 'hour', 'min', 'sec']):
        if format.count(match) > 0:
            parts.append('%.2d' % timetuple[i])
    # 2) Return time as timestamp
    if len(parts) == 0:
        return format_time(timetuple, daysep='-')
    # Return requested parts of the time
    elif len(parts) == 1:
        return parts[0]
    else:
        return parts


def _get_time():
    current = time.time()
    timetuple = time.localtime(current)[:6]  # from year to secs
    millis = int((current - int(current)) * 1000)
    timetuple += (millis,)
    return timetuple


_current_time = None


def get_timestamp(daysep='', daytimesep=' ', timesep=':', millissep='.'):
    timetuple = time.localtime()[:6]
    if _current_time is None:
        timetuple = _get_time()
    else:
        timetuple = _current_time
    return format_time(timetuple, daysep, daytimesep, timesep, millissep)


def format_time(timetuple, daysep='', daytimesep=' ', timesep=':', millissep=None):
    """Returns a timestamp formatted from timetuple using separators.

    timetuple is (year, month, day, hour, min, sec[, millis]), where parts must
    be integers and millis is required only when millissep is not None.
    """
    daytimeparts = ['%02d' % t for t in timetuple[:6]]
    day = daysep.join(daytimeparts[:3])
    time_ = timesep.join(daytimeparts[3:6])
    millis = millissep is not None and '%s%03d' % (millissep, timetuple[6]) or ''
    return day + daytimesep + time_ + millis
