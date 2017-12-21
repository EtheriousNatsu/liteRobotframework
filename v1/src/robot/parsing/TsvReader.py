#!/usr/bin/env python
# encoding: utf-8


"""
@version: 2.7
@author: 'john'
@time: 2017/10/13 下午12:02
@contact: zhouqiang847@gmail.com
"""


class TsvReader:
    """用来读取文件内容"""

    def read(self, tsvfile, rawdata):
        """"""
        process = False
        for row in tsvfile.read().splitlines():
            cells = self._get_cells(row)
            name = len(cells) > 0 and cells[0].strip() or ''
            if name.startswith('*') and rawdata.start_table(name.replace('*', '')):
                process = True
            elif process:
                rawdata.add_row(cells)

    def _get_cells(self, row):
        """把row中每个cell进行处理后形成一个列表，返回该列表"""
        return [self._process_cell(cell) for cell in row.split('\t')]

    def _process_cell(self, cell):
        """
            1、如果cell是双引号包围的，对它进行处理
            2、把cell解码成unicode，且编码为utf-8
        """
        if len(cell) > 1 and cell[0] == cell[-1] == '"':
            cell = cell[1:-1].replace('""', '"')
        return cell.decode('UTF-8')
