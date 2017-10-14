#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/1 下午12:44
@contact: zhouqiang847@gmail.com
"""

import os, re
import tempfile
import posixpath

_is_url_re = re.compile('^\w{2,}://')


def is_url(string):
    return _is_url_re.search(string) is not None


def get_not_none(*args):
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
    """Create suite name from given path that points to file or directory.

    Examples:
        '/tmp/tests.py'         -> 'Tests'
        '/var/data/my_tests/    -> 'My Tests'
        'c:\path\my_tests.html' -> 'My Tests'
        'd:\MY TESTS.HTML'      -> 'MY TESTS'
        'e:\myTestCases.html    -> 'My Test Cases'
    """
    # Get name of the file/dir without leading path and possible extension
    name = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
    return printable_name(name, code_style=True)


def _isWordBoundary(prev, char, next):
    if char.isupper():
        return (prev.islower() or next.islower()) and prev.isalnum()
    if char.isdigit():
        return prev.isalpha()
    return prev.isdigit()


def _splitCamelCaseString(string):
    parts = []
    current_part = []
    string = ' ' + string + ' '  # extra spaces make going through string easier
    for i in range(1, len(string) - 1):
        # on 1st/last round prev/next is ' ' and char is 1st/last real char
        prev, char, next = string[i - 1:i + 2]
        if _isWordBoundary(prev, char, next):
            parts.append(''.join(current_part))
            current_part = [char]
        else:
            current_part.append(char)
    parts.append(''.join(current_part))  # append last part
    return parts


def printable_name(string, code_style=False):
    """Generates and returns printable name from the given string.

    Examples:
    'simple'           -> 'Simple'
    'name with spaces' -> 'Name With Spaces'
    'more   spaces'    -> 'More Spaces'
    'Cases AND spaces' -> 'Cases AND Spaces'
    ''                 -> ''

    If 'code_style' is True:

    'mixedCAPSCamel'   -> 'Mixed CAPS Camel'
    'camelCaseName'    -> 'Camel Case Name'
    'under_score_name' -> 'Under Score Name'
    'under_and space'  -> 'Under And Space'
    'miXed_CAPS_nAMe'  -> 'MiXed CAPS NAMe'
    ''                 -> ''
    """
    if code_style:
        string = string.replace('_', ' ')
    parts = string.split()
    if len(parts) == 0:
        return ''
    elif len(parts) == 1 and code_style:
        parts = _splitCamelCaseString(parts[0])
    parts = [part[0].upper() + part[1:] for part in parts if part != '']
    return ' '.join(parts)


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
