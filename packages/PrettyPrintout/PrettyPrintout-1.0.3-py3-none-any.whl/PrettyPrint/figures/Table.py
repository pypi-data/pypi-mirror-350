import pandas
from PrettyPrint.output import Printer
from PrettyPrint.figures.Separator import separator
from PrettyPrint.format import *

class Table:
    def __init__(self, data=None, columns=None, printer=None, cell_num=None, col_width=None, cell_fmt=None, frame_fmt=None):
        # check for printer arg
        if isinstance(printer, Printer):
            self._printer = printer
        elif printer is None:
            self._printer = Printer()
        else:
            raise TypeError('printer must be a Printer or None')

        # check for dataframe
        if isinstance(data, pandas.DataFrame):
            self.df = data
            self.cols = len(self.df.columns)
        elif data is None:
            self.df = pandas.DataFrame(columns=columns, index=None)
            self.cols = len(self.df.columns)
        else:
            raise TypeError('data has to be a pandas.DataFrame or None')

        # create cell fmt list
        if cell_fmt is None:
            self.cell_fmt = ['']*self.cols
        elif isinstance(cell_fmt, PPFormat):
            self.cell_fmt = [str(cell_fmt)]*self.cols
        elif isinstance(cell_fmt, list) and all(isinstance(elem, PPFormat) for elem in cell_fmt):
            if len(cell_fmt) == self.cols:
                self.cell_fmt = cell_fmt
            else:
                raise ValueError('cell_fmt list must be same length as cols')
        else:
            raise TypeError('cell_fmt must be None, PPFormat or list of PPFormat')

        # check for df size
        if len(self.df.columns) > 10:
            raise UserWarning('Column number is large and may not fit in the console window.')

        # check for frame format
        if frame_fmt is None:
            self._vertical_sep = '|'
            self.frame_fmt = Default()
        elif isinstance(frame_fmt, PPFormat):
            self._vertical_sep = str(frame_fmt)+'|'+"\033[0m"
            self.frame_fmt = frame_fmt
        else:
            raise TypeError('frame_fmt needs to be a PPFormat or None')

        # build format string
        self._string = self._vertical_sep
        self._string += ('{}{}' + self._vertical_sep) * self.cols
        if type(cell_num) is str:
            self._cell_num = [cell_num]*self.cols
        elif cell_num is None:
            self._cell_num = ['']*self.cols
        elif isinstance(cell_num, list) and all(isinstance(elem, str) for elem in cell_num):
            if len(cell_num) == self.cols:
                self._cell_num = cell_num
            else:
                raise ValueError('cell_num list must be same length as cols')
        else:
            raise TypeError('cell_num needs to be None, a single format or a list of formats')

        # compute width
        if col_width is None:
            self._col_width = [len(elem) for elem in self.df.columns]
        elif type(col_width) is int:
            self._col_width = [col_width for elem in self.df.columns]
        elif isinstance(col_width, list) and all(isinstance(elem, int) for elem in col_width):
            if len(col_width) == self.cols:
                self._col_width = col_width
            else:
                raise ValueError('col_width list must be same length as cols')
        else:
            raise TypeError('col_width needs to be a list of integers, an integer or none')

        self._table_width = sum(self._col_width)+1+self.cols

        if data is not None:
            self._print_table()
        else:
            self._print_header()


    def add_row(self, series):
        # add new row to df, call print_row after to print to console
        if len(series) == self.cols:
            self.df.loc[len(self.df.index)] = series
            self._print_row(-1)
        else:
            raise ValueError('Series and table of unequal length.')

    def _resize_cell(self, idx, content):
        if self._col_width[idx] < len(content):
            return content[:self._col_width[idx]]
        elif self._col_width[idx] > len(content):
            padding = self._col_width[idx] - len(content)
            return ' ' * padding + content
        else:
            return content

    def _parse_row(self, idx): # uses pd series objects
        series = self.df.iloc[idx]
        args = []
        for i in range(len(series)):
            args.append(self.cell_fmt[i])
            args.append(self._resize_cell(i, ('{'+self._cell_num[i]+'}').format(series.iloc[i])))
        row_string = self._string.format(*args)
        return row_string

    def _parse_header(self): # parses the header to the specified format
        header_string = self._vertical_sep+('{}{}'+self._vertical_sep)*self.cols
        args = []
        for i in range(self.cols):
            args.append(self.cell_fmt[i])
            args.append(self._resize_cell(i, self.df.columns[i]))
        row_string = header_string.format(*args)
        return row_string

    def _print_sep(self):
        self._printer(separator(self._table_width), fmt=self.frame_fmt)

    def _print_header(self):
        self._print_sep()
        head_str = self._parse_header()  # build row string
        self._printer(head_str)
        self._print_sep()

    def _print_row(self, idx):
        row_str = self._parse_row(idx) # build row string
        self._printer(row_str)
        self._print_sep()

    def _print_table(self):
        self._print_header()
        for i in range(len(self.df.index)):
            self._print_row(i)


