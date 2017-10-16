#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/16 下午9:27
@contact: zhouqiang847@gmail.com
"""



from robot.common.keyword import BaseKeyword


def KeywordList(rawkeywords):
    keywords = []
    # block = None
    for row in rawkeywords:
        # if len(row) == 0:
        #     continue
        # if block is not None and row[0] == '':
        #     block.add_row(row[1:])
        # else:
        #     try:
        #         kw = block = BlockKeywordFactory(row)
        #     except TypeError:
        #         kw = KeywordFactory(row)
        #         block = None
        kw = KeywordFactory(row)
        keywords.append(kw)
    return keywords



def KeywordFactory(kwdata):
    # try:
    #     try:
    #         return SetKeyword(kwdata)
    #     except TypeError:
    #         pass
    #     try:
    #         return RepeatKeyword(kwdata)
    #     except TypeError:
    #         pass
    # except:
    #     return SyntaxErrorKeyword(kwdata, utils.get_error_message())
    return BaseKeyword(kwdata[0], kwdata[1:])