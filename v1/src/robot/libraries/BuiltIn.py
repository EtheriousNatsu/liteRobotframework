"""
fsfsfsd
"""


class _Converter(object):
    """ this is a test """

    def convert_to_boolean(self, item):
        """convert given item to a boolean"""
        if isinstance(item, basestring):
            if item.upper() == 'TRUE':
                return True
            if item.upper() == 'FALSE':
                return False
        try:
            return bool(item)
        except:
            raise Exception("%s can not convert to a boolean" % item)

    def create_list(self, *items):
        """Returns a list containing given items.

                The returned list can be assigned both to ${scalar} and @{list}
                variables. The earlier can be used e.g. with Java keywords expecting an array as an
                argument.

                Examples:
                | @{list} =   | Create List | a    | b    | c    |
                | ${scaler} = | Create List | a    | b    | c    |
                | ${ints} =   | Create List | ${1} | ${2} | ${3} |
        """
        try:
            return list(items)
        except:
            pass


class _Verify(object):
    def get_length(self, item):
        """Returns the length of the given item.

                The keyword first tries to get the length with the Python function 'len',
                which calls the item's '__len__' method internally. If that fails, the
                keyword tries to call the item's 'length' and 'size' methods directly.
                The final attempt is trying to get the value of the item's 'length'
                attribute. If all these attempts are unsuccessful, the keyword fails.

                New in Robot Framework version 1.8.2.
        """
        try:
            return len(item)
        except:
            pass
        try:
            return item.length()
        except:
            pass
        try:
            return item.length
        except:
            raise Exception("Could not get length of '%s" % item)

    def should_be_true(self, expr, msg=None):
        """Fails if the given expression (or item) is not true.

                If 'expr' is a string (e.g. '${rc} < 10'), it is evaluated as a Python
                expression using the built-in 'eval' function and the keyword status is
                decided based on the result. If a non-string item is given, the status
                is got directly from its truth value as explained at
                http://docs.python.org/lib/truth.html.

                The default error message ('<expr> should be true') maybe is not very
                informative, but it can be overridden with the 'msg' argument.

                Examples:
                | Should Be True | ${rc} < 10  |
                | Should Be True | '${status}' == 'PASS' | # Strings must be quoted |
                | Should Be True | ${number}   | # Passes if ${number} is not zero |
                | Should Be True | ${list}     | # Passes if ${list} is not empty  |

                New in Robot Framework version 1.8.3. This is intended to replace the
                old keyword 'Fail Unless', which still continues to work.
        """
        if msg is None:
            msg = "%s should be true" % expr
        if not isinstance(expr, basestring):
            raise Exception("%s should be str" % expr)
        if not bool(eval(expr)):
            raise AssertionError(msg)

    def should_contain(self, str1, str2, msg=None):
        """Fails if the string 'str1' does not contain the string 'str2' one or more times.

                See 'Should Be Equal' for an explanation on how to override the default
                error message with 'msg' and 'values'.
        """
        msg = self._get_string_msg(str1, str2, msg, "does not contain")
        if str1.count(str2) < 1:
            raise AssertionError(msg)

    def should_not_be_empty(self, item, msg=None):
        """Verifies that the given item is not empty.

                The length of the item is got using the 'Get Length' keyword. The
                default error message can be overridden with the 'msg' argument.

                New in Robot Framework version 1.8.2.
        """
        if self.get_length(item) == 0:
            if msg is None:
                msg = "%s should not be empty" % item
            raise AssertionError(msg)

    def _get_string_msg(self, str1, str2, msg, delim):
        _msg = "%s %s %s" % (str1, delim, str2)
        if msg is None:
            msg = _msg
        return msg


class BuiltIn(_Converter, _Verify):
    pass
