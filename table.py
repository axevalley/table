#!/usr/bin/python3

#Table by Luke Shiner (luke@lukeshiner.com)

import csv

from . tablerow import TableRow


class Table(object):
    """ Container for tabulated data. Can be created from a .csv by
    passing the file path to __init__.
    """

    
    def __init__(self, filename=None):
        self.empty()

        if isinstance(filename, str):
            self.openFile(filename)
    

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
        return 'CsvFile Object containing ' + columns + ' colomuns and ' + rows + ' rows. ' + total + ' total entries.'

    def openFile(self, filename):
        """ Creates Table object from a .csv file. This file must be
        comma separated and utf-8 encoded. The first row must contain
        column headers.
        
        If the object already contains date it will be overwritten.
        """

        assert self.isEmpty(), 'Only empty Table objects can open files'
        
        csvFile = open(filename, 'rU', encoding='utf-8', errors='replace')
        csvFile = csv.reader(csvFile)
        i = 0
        for row in csvFile:
            if i == 0:
                self.header = row
                i += 1
            else:
                self.rows.append(TableRow(row, self.header))
            
        self.setTable()

    def loadFromDatabaseTable(self, databaseTable):
        """ Loads data from a MySQL table contained in a DatabaseTable
        object.
        """
        assert self.isEmpty(), 'Only empty Table objects can load from a database'
        #assert isinstance(databaseTable, stctools.DatabaseTable), 'databaseTable must be instance of stctools.DatabaseTable'
        
        self.header = databaseTable.getColumns()
        data = databaseTable.getAll()
        for row in data:
            self.rows.append(TableRow(row, self.header))

        self.setTable()

    def empty(self):
        """ Clears all data from the Table. The same as initialising a
        new Table with no arguments.
        """
        
        self.rows = []
        self.header = []
        self.columns = []
        self.headers = {}

    def setHeaders(self):
        """ Creates a dictionary of headers for looking up the
        apropriate index in self.columns.
        """
        
        self.headers = {}
        for column in self.header:
            self.headers[column] = self.header.index(column)

    def setColumns(self):
        """ Creates a 2d list pivoted from self.rows.  """
        self.columns = []
        columnNumber=0
        for column in self.header:
            thisColumn = []
            rowNumber=0
            for row in self.rows:
                thisColumn.append(self.rows[rowNumber][columnNumber])
                rowNumber += 1
            self.columns.append(thisColumn)
            columnNumber += 1

    def setTable(self):
        self.setHeaders()
        self.setColumns()            
    

    def isEmpty(self):
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
        
        assert isinstance(row, list) or isinstance(row, TableRow), 'New Row must be list or TableRow'
        if isinstance(row, list):
            assert len(row) == len(self.header), 'New Row must have correct number of entries'
            self.rows.append(TableRow(row, self.header))
            self.setTable()
        elif isinstance(row, TableRow):
            assert row.header == self.header, 'New Row must have correct header'
            self.rows.append(row)

    def getColumn(self, column):
        """ Returns a list containing all values from the specified
        column.
        """
        
        return self.columns[self.headers[column]]

    def removeColumn(self, column):
        """ Removes a specified column from the Table.  """
        if column in self.header:
            for row in self.rows:
                row.removeColumn(column)                
            self.setHeaders()
            self.setColumns()
            print('DELETED column: ' + column)
        else:
            return False
        
    def getRows(self):
        return self.rows

    def loadFromArray(self, data, header):
        """ Loads the Table with data contained in a 2d list
        object.
        """

        assert self.isEmpty(), 'Only empty Table objects can open files'
        assert isinstance(header, list), 'header must be list containing column headers'
        assert isinstance(data, list), 'data must be list'
        for row in data:
            assert isinstance(row, list) or isinstance(row, TableRow), 'data must contain list or TableRow'
            if isinstance(row, list):
                assert len(row) == len(header)
            else:
                #assert row.header == self.header, 'New Row must have correct header'
                pass

        self.header = header

        for row in data:
            if isinstance(row, TableRow):
                self.rows.append(row)
            else:
                self.rows.append(TableRow(row, header))

        self.setTable()

    def write(self, filename):
        """ Creates a .csv of the data contained within the Table with
        the specifed filename or filepath.
        This file will be comma separated and UTF-8 encoded.
        """
        
        file = open(filename, 'w', newline='', encoding='UTF-8')
        writer = csv.writer(file)
        writer.writerow(self.header)
        for row in self:
            writer.writerow(row.toArray())
        file.close()
        print('Writen ' + str(len(self.rows)) + ' lines to file ' + filename)
