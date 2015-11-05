#!/usr/bin/python3

# Table by Luke Shiner (luke@lukeshiner.com)

import csv

from . tablerow import TableRow


class Table(object):
    """ Container for tabulated data. Can be created from a .csv by
    passing the file path to __init__.
    """

    def __init__(self, filename=None):
        self.empty()

        if isinstance(filename, str):
            self.open_file(filename)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        for row in self.rows:
            yield row

    def __getitem__(self, index):
        return self.rows[index]

    def __str__(self):
        columns = str(len(self.columns))
        rows = str(len(self.rows))
        total = str(len(self.columns) * len(self.rows))
        string = 'CsvFile Object containing ' + columns + ' colomuns and '
        string = string + rows + ' rows. ' + total + ' total entries.'
        return string

    def open_file(self, filename):
        """ Creates Table object from a .csv file. This file must be
        comma separated and utf-8 encoded. The first row must contain
        column headers.

        If the object already contains date it will be overwritten.
        """

        assert self.is_empty(), 'Only empty Table objects can open files'

        csv_file = open(filename, 'rU', encoding='utf-8', errors='replace')
        csv_file = csv.reader(csv_file)
        i = 0
        for row in csv_file:
            if i == 0:
                self.header = row
                i += 1
            else:
                self.rows.append(TableRow(row, self.header))

        self.set_table()

    def load_from_database_table(self, database_table):
        """ Loads data from a MySQL table contained in a DatabaseTable
        object.
        """
        assert self.is_empty(), (
            'Only empty Table objects can load from a database')
        # assert isinstance(database_table, stctools.DatabaseTable), (
        # 'database_table must be instance of stctools.DatabaseTable')

        self.header = database_table.get_columns()
        data = database_table.get_all()
        for row in data:
            self.rows.append(TableRow(row, self.header))

        self.set_table()

    def empty(self):
        """ Clears all data from the Table. The same as initialising a
        new Table with no arguments.
        """

        self.rows = []
        self.header = []
        self.columns = []
        self.headers = {}

    def set_headers(self):
        """ Creates a dictionary of headers for looking up the
        apropriate index in self.columns.
        """

        self.headers = {}
        for column in self.header:
            self.headers[column] = self.header.index(column)

    def set_columns(self):
        """ Creates a 2d list pivoted from self.rows.  """
        self.columns = []
        column_number = 0
        for column in self.header:
            thisColumn = []
            rowNumber = 0
            for row in self.rows:
                thisColumn.append(self.rows[rowNumber][column_number])
                rowNumber += 1
            self.columns.append(thisColumn)
            column_number += 1

    def set_table(self):
        self.set_headers()
        self.set_columns()

    def is_empty(self):
        """ Returns True if the table conatins no data, otherwise
        returns False.
        """
        if self.rows == []:
            if self.header == []:
                if self.columns == []:
                    return True
        return False

    def append(self, row):
        """ Creates a new row in the Table from a TableRow object or
        creates one from a list object with the correct number of
        values.
        """
        assert isinstance(row, list) or isinstance(row, TableRow), (
            'New Row must be list or TableRow')
        if isinstance(row, list):
            assert len(row) == len(self.header), (
                'New Row must have correct number of entries')
            self.rows.append(TableRow(row, self.header))
            self.set_table()
        elif isinstance(row, TableRow):
            assert row.header == self.header, (
                'New Row must have correct header')
            self.rows.append(row)

    def get_column(self, column):
        """ Returns a list containing all values from the specified
        column.
        """

        return self.columns[self.headers[column]]

    def remove_column(self, column):
        """ Removes a specified column from the Table.  """
        if column in self.header:
            for row in self.rows:
                row.remove_column(column)
            self.set_headers()
            self.set_columns()
            print('DELETED column: ' + column)
        else:
            return False

    def getRows(self):
        return self.rows

    def load_from_array(self, data, header):
        """ Loads the Table with data contained in a 2d list
        object.
        """

        assert self.is_empty(), 'Only empty Table objects can open files'
        assert isinstance(header, list), (
            'header must be list containing column headers')
        assert isinstance(data, list), 'data must be list'
        for row in data:
            assert isinstance(row, list) or isinstance(row, TableRow), (
                'data must contain list or TableRow')
            if isinstance(row, list):
                assert len(row) == len(header)
            else:
                # assert row.header == self.header, (
                # 'New Row must have correct header')
                pass

        self.header = header

        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow(row, header))

        self.set_table()

    def write(self, filename):
        """ Creates a .csv of the data contained within the Table with
        the specifed filename or filepath.
        This file will be comma separated and UTF-8 encoded.
        """

        file = open(filename, 'w', newline='', encoding='UTF-8')
        writer = csv.writer(file)
        writer.writerow(self.header)
        for row in self:
            writer.writerow(row.to_array())
        file.close()
        print('Writen ' + str(len(self.rows)) + ' lines to file ' + filename)

    def to_html(self, header=True):
        """ Returns a string containg the data held in the Table as
        as html table.
        If header=True the column headings will be included in <th>
        tags. If it is False no headings will be written.
        """
        open_table = '<table>\n'
        close_table = '</table>\n'
        open_tr = '\t<tr>\n'
        close_tr = '\t</tr>\n'
        open_th = '\t\t<th>'
        close_th = '</th>\n'
        open_td = '\t\t<td>'
        close_td = '</td>\n'
        html_table = ''
        html_table += open_table
        if header:
            html_table += open_tr
            for head in self.header:
                html_table += open_th
                html_table += head
                html_table += close_th
            html_table += close_tr
        for row in self.rows:
            html_table += open_tr
            for cell in row:
                html_table += open_td
                html_table += cell
                html_table += close_td
            html_table += close_tr
        html_table += close_table
        return html_table

    def to_html_file(self, filename, header=True):
        html_file = open(filename, 'w', encoding='utf-8')
        html_file.write(self.to_html(header=header))
        html_file.close()

    def print_r(self):
        for row in self.rows:
            print(row.row)

    def copy(self):
        new_table = Table()
        new_table.header = self.header
        for row in self.rows:
            new_table.rows.append(row.copy())
        new_table.set_table()
        return new_table

    def sort(self, sort_key, asc=True):
        if type(sort_key) == str:
            if sort_key in self.header:
                column = self.header.index(sort_key)
            else:
                raise KeyError('sort_key must be int or in header')
        else:
            column = sort_key
        try:
            self.rows.sort(key=lambda x: float(x.row[column]), reverse=not asc)
        except ValueError:
            self.rows.sort(key=lambda x: x.row[column], reverse=not asc)

    def sorted(self, sort_key, asc=True):
        temp_table = self.copy()
        temp_table.sort(sort_key, asc)
        return temp_table

    def multi_sort_direction(self, sort_direction):
        if type(sort_direction) == str:
            if sort_direction.upper() not in ('A', 'ASC', 'ASCENDING',
                                              'D', 'DESC',
                                              'DESCENDING'):
                raise Exception(
                    "sort_direction must be one of 'A', 'ASC'," +
                    " 'ASCENDING', 'D', 'DESC', 'DESCENDING'")
        elif type(sort_direction) != bool:
            raise TypeError('sort_direction must be str or bool')
        if type(sort_direction) == str:
            if sort_direction in ('A', 'ASC', 'ASCENDING'):
                return True
            elif sort_direction in ('D', 'DESC', 'DESCENDING'):
                return False

    def multi_sort_validate(self, sort_key):
        if type(sort_key) not in (int, str):
            raise TypeError('sort_key Must be int')
        if sort_key not in self.header:
            raise KeyError('sort_key must be in header')
        return True

    def multi_sort(self, *sort_keys):
        if type(sort_keys) in (list, tuple):
            if type(sort_keys[0]) in (list, tuple):
                sort_keys = reversed(sort_keys)
        for sort_pair in sort_keys:
            if type(sort_pair) in (str, int):
                sort_key = sort_pair
            elif type(sort_pair) in (list, tuple):
                sort_key, sort_direction = sort_pair
            else:
                raise TypeError(
                    'sort_keys must be int, str, list or tuple. Not ' +
                    str(type(sort_pair)))
            if self.multi_sort_validate(sort_key):
                asc = self.multi_sort_direction(sort_direction)
                self.sort(sort_key, asc)

    def multi_sorted(self, *sort_keys):
        temp_table = self.copy()
        temp_table.multi_sort(*sort_keys)
        return temp_table
