import numpy as np
import math as math
import copy as copy



class Matrix:
    def __init__(self, edges:list[list[float]]):

        self.matrix = np.array(edges).astype(float)
        self.size = self.matrix.shape[0] # should just be the same shape, so we can just use the first value

        # experimental lower cost sets
        self.searchable_rows = {i for i in range(self.size)}
        self.searchable_cols = {j for j in range(self.size)}
        self.zero_out_middle() # makes sure we don't just loop back on itself

        self._lower_bound = self.calculate_lower_bound()

    def __hash__(self):
        return hash(self.matrix.tobytes())

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return np.array_equal(self.matrix, other.matrix)
        return False

# basics for messing around with the matrix

    def get_matrix(self):
        return self.matrix

    def get_lower_bound(self):
        return self._lower_bound

    # special row operations V
    def set_row_inf(self, row: int):
        for element in range(len(self.matrix[row])):
            if self.matrix[row][element] == 0:
                self.searchable_cols.add(element) # there may have been a change inside of our data structure that we need to account for
            self.matrix[row][element] = math.inf

    def set_column_inf(self, column: int):
        for element in range(len(self.matrix[:, column])):
            if self.matrix[element][column] == 0:
                self.searchable_rows.add(element)
            self.matrix[element][column] = math.inf

    def select_val(self, row:int, col:int):
        value = self.matrix[row][col]

        # set the value to infinity, as well as it's reciprocal
        self.matrix[row][col] = math.inf
        self.matrix[col][row] = math.inf

        return value

    # this is the main algorithm that allows you to reduce find a reduced matrix

    def zero_out_middle(self):
        for i in range (self.size):
            self.matrix[i][i] = math.inf

    # Note, will change the matrix it is called on
    def calculate_lower_bound(self):
        total_score = 0

        zero_rows = set()
        for i in self.searchable_rows: # O(n^2) for finding the min
            min_val = min(self.matrix[i]) # get the minimum value in that row

            if min_val == math.inf:
                self.searchable_rows.remove(i) # if a row or column is infinity, then stop searching it
                return math.inf

            self.matrix[i] -= min_val # subtract the minimum value from the row
            zero_rows.add(i) # means that that are minimum value is now zero and will be until things change
            total_score += min_val

        self.searchable_rows.difference_update(zero_rows) # remove the rows that are zeroed out
        del zero_rows

        zero_cols = set()
        for j in self.searchable_cols:
            min_val = min(self.matrix[:,j])

            if min_val == math.inf:
                self.searchable_cols.remove(j)
                return math.inf # possibly put a return statement here because you don't need to search it

            self.matrix[:,j] -= min_val
            zero_cols.add(j)
            total_score += min_val

        self.searchable_cols.difference_update(zero_cols)
        del zero_cols

        return total_score # fin

    # do we or do we not reduce the cost at the beginning of the algorithm?
    def reduced_cost_matrix(self,coming_from:int,going_to:int):
        copy_matrix = copy.deepcopy(self) # O(1)
        remaining_path_cost = copy_matrix.select_val(coming_from, going_to) # O(1)

        # set the rows and columns to infinity
        copy_matrix.set_row_inf(coming_from) # O(n)
        copy_matrix.set_column_inf(going_to) # O(n)

        update_cost = copy_matrix.calculate_lower_bound() # O(n^2)
        copy_matrix._lower_bound += update_cost + remaining_path_cost # O(1)

        return copy_matrix
