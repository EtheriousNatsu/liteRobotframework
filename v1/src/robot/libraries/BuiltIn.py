"""
fsfsfsd
"""


class Converter(object):
    """ this is a test """

    def convert_to_integer(self, item):
        """convert given item to a long integer"""
        try:
            return long(item)
        except:
            raise Exception("%s can not convert to a long integer" % item)

    def convert_to_number(self, item):
        """ convert given item to an integer"""
        try:
            return int(item)
        except:
            raise Exception("%s can not convert to an integer" % item)

    def convert_to_boolean(self, item):
        """convert given item to a boolean"""
        try:
            return bool(item)
        except:
            raise Exception("%s can not convert to a boolean" % item)

    def create_list(self):
        """
        """
        pass
