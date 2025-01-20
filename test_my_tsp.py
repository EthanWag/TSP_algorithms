import unittest
import numpy as np
import math as math

from test_tsp import assert_valid_tours
from tsp_core import Timer, generate_network, score_tour

from matrix import Matrix
from greedy import find_greedy
from dfs import find_dfs

if __name__ == '__main__':
    unittest.main()

# Tests the matrix class

def test_initial_bound():

    matrix = Matrix([[math.inf,9,math.inf,8,math.inf],
                     [math.inf,math.inf,4,math.inf,2],
                     [math.inf,3,math.inf,4,math.inf],
                     [math.inf,6,7,math.inf,12],
                     [1,math.inf,math.inf,10,math.inf]])
    assert 21 == matrix.get_lower_bound()

def test_other_bound():

    matrix = Matrix([[math.inf,8,12,4],
                     [3,math.inf,7,1],
                     [2,6,math.inf,4],
                     [math.inf,3,5,math.inf]])

    assert 12 == matrix.get_lower_bound()

def test_reduced_cost_matrix():
    matrix = Matrix([[math.inf,1,math.inf,0,math.inf],
                     [math.inf,math.inf,1,math.inf,0],
                     [math.inf,0,math.inf,1,math.inf],
                     [math.inf,0,0,math.inf,6],
                     [0,math.inf,math.inf,9,math.inf]])
    new_matrix = matrix.reduced_cost_matrix(0,1)
    assert new_matrix.get_lower_bound() == 2

# mimics the algorithm found in the slides
def test_mock_partial_path():
    matrix = Matrix([[math.inf, 9, math.inf, 8, math.inf],
                     [math.inf, math.inf, 4, math.inf, 2],
                     [math.inf, 3, math.inf, 4, math.inf],
                     [math.inf, 6, 7, math.inf, 12],
                     [1, math.inf, math.inf, 10, math.inf]])

    matrix_dict = {int:Matrix}
    cost_list = []


    for i in range(matrix.size):

        new_matrix = matrix.reduced_cost_matrix(0,i)

        cost_list.append(new_matrix.get_lower_bound())
        matrix_dict[i] = new_matrix

    assert 21 == min(cost_list)


# Tests the greedy class for optimal solution

def test_greedy():
    graph = [
        [0, 9, math.inf, 8, math.inf],
        [math.inf, 0, 4, math.inf, 2],
        [math.inf, 3, 0, 4, math.inf],
        [math.inf, 6, 7, 0, 12],
        [1, math.inf, math.inf, 10, 0]
    ]

    timer = Timer(1000)
    stats = find_greedy(graph,timer)
    assert stats[0].tour == [1, 4, 0, 3, 2]
    assert stats[0].score == 21



def test_dfs():
    graph = [
        [0, 9, math.inf, 8, math.inf],
        [math.inf, 0, 4, math.inf, 2],
        [math.inf, 3, 0, 4, math.inf],
        [math.inf, 6, 7, 0, 12],
        [1, math.inf, math.inf, 10, 0]
    ]
    timer = Timer(10000)
    stats = find_dfs(graph, timer)
    assert stats[0].tour == [0, 3, 2, 1, 4]
    assert stats[0].score == 21

