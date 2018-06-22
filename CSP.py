__author__ = "Paweł Bernecki"

from collections import deque
import copy
import random

import numpy as np
import Field


class CSP:
    def __init__(self, task=0, size=4):
        self.task = task
        self.size = size
        self.results = deque()
        self.iterations_bt = 0
        self.iterations_fc = 0

    def start(self, algorithm=1):
        variables = deque()
        if (self.task == 0):  # N queens
            array = np.zeros(shape=self.size, dtype=int)
            array[:] = [x - 10 for x in array]
            def forwardchecking(*args):
                return self.forwardchecking_queens(args[0], args[1])
            def backtracking(*args):
                return self.backtracking_queens(args[0], args[1])
            for i in range(self.size):
                variables.append(Field.Field(0, i, self.size, 0))
        else:  # Latin square
            array = np.zeros(shape=(self.size, self.size), dtype=int)
            def forwardchecking(*args):
                return self.forwardchecking_latin(args[0], args[1])
            def backtracking(*args):
                return self.backtracking_latin(args[0], args[1])
            for i in range(self.size):
                for j in range(self.size):
                    variables.append(Field.Field(i, j, self.size, 1))
        if algorithm == 0:
            forwardchecking(copy.deepcopy(array), copy.deepcopy(variables))
            iterations = self.iterations_fc
        elif algorithm == 1:
            backtracking(array, variables)
            iterations = self.iterations_bt
        else:
            print("normal bt")
            self.singlebacktrackqueens(copy.deepcopy(array), copy.deepcopy(variables))
            random.shuffle(variables)
            print("random bt")
            self.iterations_bt = 0
            self.singlebacktrackqueens(array, variables)
            iterations = -1
        return (self.results, iterations)

    def modify_domains_latin(self, variables, current_variable, value):
        for var in variables:
            if var.column == current_variable.column or var.row == current_variable.row:
                if value in var.domain:
                    var.domain.remove(value)
        return variables

    def forwardchecking_latin(self, array, variables):
        if (len(variables) == 0):
            self.results.append(copy.copy(array))
            return True
        variable = variables.popleft()
        for value in variable.domain:
            for var in variables:
                if not var.domain:
                    return False
            variables_temp = self.modify_domains_latin(copy.deepcopy(variables), variable, value)
            array[variable.row, variable.column] = value
            self.forwardchecking_latin(array, variables_temp)
            self.iterations_fc += 1
            array[variable.row, variable.column] = 0
        return False

    def backtracking_latin(self, array, variables):
        if self.check_latin(array):
            self.results.append(copy.copy(array))
            return True
        if (len(variables) == 0):
            return False
        variable = variables.popleft()
        for value in variable.domain:
            if self.check_consistancy_latin(array, variable.row, variable.column, value):
                array[variable.row, variable.column] = value
                self.backtracking_latin(array, copy.copy(variables))
                self.iterations_bt += 1
                array[variable.row, variable.column] = 0
        return False

    def check_consistancy_latin(self, array, row, col, val):
        if val in array[row] or val in array[:, col]:
            return False
        return True

    def check_latin(self, array):
        for i in range(self.size):
            if len(np.unique(array[i])) != self.size or 0 in array[i]:
                return False
            if len(np.unique(array[:, i])) != self.size or 0 in array[:, i]:
                return False
        return True

    def modify_domains_queens(self, variables, current_variable, value):
        for var in variables:
            if value in var.domain:
                var.domain.remove(value)
            if value + var.column - current_variable.column in var.domain:
                var.domain.remove(value + var.column - current_variable.column)
            if value - var.column + current_variable.column in var.domain:
                var.domain.remove(value - var.column + current_variable.column)
        return variables

    def forwardchecking_queens(self, array, variables):
        if len(variables) == 0:
            self.results.append(copy.copy(array))
            return True
        variable = variables.popleft()
        for value in variable.domain:
            for var in variables:
                if not var.domain:
                    return False
            variables_temp = self.modify_domains_queens(copy.deepcopy(variables), variable, value)
            array[variable.column] = value
            self.forwardchecking_queens(array, variables_temp)
            self.iterations_fc += 1
            array[variable.column] = -10
        return False

    def backtracking_queens(self, array, variables):
        if self.check_queens(array):
            self.results.append(copy.copy(array))
            return True
        if (len(variables) == 0):
            return False
        variable = variables.popleft()
        for value in variable.domain:
            if self.check_consistancy_queens(array, variable.column, value):
                self.backtracking_queens(array, copy.copy(variables))
                self.iterations_bt += 1
                array[variable.column] = -10
        return False

    def check_consistancy_queens(self, array, col, val):
        for i in range(len(array)):
            dr = val - array[i]
            dc = col - i
            if dr == dc or dr == -dc:
                return False

        if val in array:
            return False
        array[col] = val
        diffs = np.diff(array)
        if 1 in diffs or -1 in diffs:
            array[col] = -10
            return False
        return True

    def check_queens(self, array):
        diffs = np.diff(array)
        if 1 in diffs or -1 in diffs or 0 in diffs or -10 in array:
            return False
        return True


    def singlebacktrackqueens(self, array, variables):
        if self.check_queens(array):
            print(self.iterations_bt)
            print(array, "\n")
            return True
        if (len(variables) == 0):
            return False
        variable = variables.popleft()
        for value in variable.domain:
            if self.check_consistancy_queens(array, variable.column, value):
                if self.singlebacktrackqueens(array, copy.copy(variables)):
                    return True
                self.iterations_bt += 1
                array[variable.column] = -10
        return False

    def singleforwardcheckqueens(self, array, variables):
        if len(variables) == 0:
            print(self.iterations_fc)
            print(array, "\n")
            return True
        variable = variables.popleft()
        for value in variable.domain:
            for var in variables:
                if not var.domain:
                    return False
            variables_temp = self.modify_domains_queens(copy.deepcopy(variables), variable, value)
            array[variable.column] = value
            if self.singlebacktrackqueens(array, variables_temp):
                return True
            self.iterations_fc += 1
            array[variable.column] = -10
        return False