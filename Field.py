__author__ = "Paweł Bernecki"

from collections import deque


class Field:
    def __init__(self, row, column, size=0, field_type=0):
        self.row = row
        self.column = column
        if field_type == 0:  # N queens
            self.domain = deque()
            for i in range(size):
                self.domain.append(i)
        else:  # Latin
            self.domain = deque()
            for i in range(1, size + 1):
                self.domain.append(i)
