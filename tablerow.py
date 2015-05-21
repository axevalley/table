#!/usr/bin/python3

#TableRow by Luke Shiner (luke@lukeshiner.com)
    
class TableRow(object):
    """ Container for a row of data. Used by Table object. """
    
    def __init__(self, row, header):
        self.row = row
        self.header = header
        self.headers = {}
        
        for column in self.header:
            self.headers[column] = self.header.index(column)
    
    
    def __iter__(self):
        for item in self.row:
            yield item

    def __getitem__(self, index):
        if type(index) == int:
            return self.row[index]
        elif type(index) == str:
            return self.row[self.headers[index]]

    def __str__(self):
        return self.to_array()

    def __len__(self):
        return len(self.row)

    def get_column(self, column):
        """ Returns the value held in the specified column.  """
        return self.row[self.headers[column]]

    def remove_column(self, column):
        """ Removes the specified column.  """
        if column in self.header:
            columnIndex = self.header.index(column)
            self.row.pop(columnIndex)
            self.header.pop(columnIndex)
        else:
            return False

    def to_array(self):
        """ Returns the data row as a list object.  """
        return self.row