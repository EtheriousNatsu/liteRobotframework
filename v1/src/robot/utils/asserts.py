#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/4 上午10:50
@contact: zhouqiang847@gmail.com
"""

def fail(msg=None):
    """Fail test immediately with the given message."""
    _report_failure(msg)


def error(msg=None):
    """Error test immediately with the given message."""
    _report_error(msg)

def fail_if(expr, msg=None):
    """Fail the test if the expression is True."""
    if expr:
        _report_failure(msg)


def fail_unless(expr, msg=None):
    """Fail the test unless the expression is True."""
    if not expr:
        _report_failure(msg)

def fail_if_none(obj, msg=None, values=True):
    """Fail the test if given object is None."""
    _msg= 'is None'
    if obj is None:
        if msg is None:
            msg = _msg
        elif values is True:
            msg = '%s: %s' % (msg, _msg)
        _report_failure(msg)

def fail_unless_none(obj, msg=None, values=True):
    """Fail the test if given object is not None."""
    _msg = '%r is not None' % obj
    if obj is not None:
        if msg is None:
            msg = _msg
        elif values is True:
            msg = '%s: %s' % (msg, _msg)
        _report_failure(msg)

def fail_unless_raises(exc_class, callable_obj, *args, **kwargs):
    """Fail unless an exception of class exc_class is thrown by callable_obj.

        callable_obj is invoked with arguments args and keyword arguments
        kwargs. If a different type of exception is thrown, it will not be
        caught, and the test case will be deemed to have suffered an
        error, exactly as for an unexpected exception.
    """
    try:
        callable_obj(*args, **kwargs)
    except exc_class:
        return
    else:
        if hasattr(exc_class, '__name__'):
            exc_name = exc_class.__name__
        else:
            exc_name = str(exc_class)
        _report_failure('%s not raised' % exc_name)


def fail_unless_raises_with_msg(exc_class, expected_msg, callable_obj, *args,
                                **kwargs):
    """Similar to fail_unless_raises but also checks the exception message."""
    try:
        callable_obj(*args, **kwargs)
    except exc_class, err:
        assert_equal(expected_msg, str(err), 'Correct exception but wrong message')
    else:
        if hasattr(exc_class,'__name__'):
            exc_name = exc_class.__name__
        else:
            exc_name = str(exc_class)
        _report_failure('%s not raised' % exc_name)


def fail_unless_equal(first, second, msg=None, values=True):
    """Fail if given objects are unequal as determined by the '==' operator."""
    if not first == second:
        _report_unequality_failure(first, second, msg, values, '!=')


def fail_if_equal(first, second, msg=None, values=True):
    """Fail if given objects are equal as determined by the '==' operator."""
    if first == second:
        _report_unequality_failure(first, second, msg, values, '==')


# def fail_unless_almost_equal(first, second, places=7, msg=None, values=True):
#     """Fail if the two objects are unequal after rounded to given places.
#
#         Unequality is determined by object's difference rounded to the
#         given number of decimal places (default 7) and comparing to zero.
#         Note that decimal places (from zero) are usually not the same as
#         significant digits (measured from the most signficant digit).
#     """




# Synonyms for assertion methods

assert_equal = assert_equals = fail_unless_equal
assert_not_equal = assert_not_equals = fail_if_equal
# assert_almost_equal = assert_almost_equals = fail_unless_almost_equal
# assert_not_almost_equal = assert_not_almost_equals = fail_if_almost_equal
assert_raises = fail_unless_raises
assert_raises_with_msg = fail_unless_raises_with_msg
assert_ = assert_true = fail_unless
assert_false = fail_if
assert_none = fail_unless_none
assert_not_none = fail_if_none


# Helpers

def _report_failure(msg):
    if msg is None:
        raise AssertionError()
    raise AssertionError(msg)


def _report_error(msg):
    if msg is None:
        raise Exception()
    raise Exception(msg)

def _report_unequality_failure(obj1, obj2, msg, values, delim, extra=None):
    if msg is None:
        msg = '%s %s %s' % (obj1, delim, obj2)
    elif values is True:
        msg = '%s %s %s %s' % (msg, obj1, delim, obj2)
    if values is True and extra is not None:
        msg += ' ' + extra
    _report_failure(msg)