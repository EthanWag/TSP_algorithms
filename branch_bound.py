from tsp_core import Timer, SolutionStats, score_tour
from tsp_cuttree import CutTree
from record import Record
from matrix import Matrix
from greedy import find_greedy

import math as math


def find_branch_bound(edges: list[list[float]], timer: Timer, my_queue,start) -> list[SolutionStats]:

    # setting up important values
    log = Record() #O(1)
    greedy_solution = find_greedy(edges, timer) #O(n^2)
    BSSF = greedy_solution[-1].score #O(1)
    log.log_status(greedy_solution[-1].tour, BSSF, timer.time(), my_queue.size(), 0, 0, CutTree(len(edges)))

    prune_tree = CutTree(len(edges))
    nodes_pruned = 0
    nodes_extended = 0

    matrix = Matrix(edges) # O(n^2)
    my_queue.push([start],matrix,0)

    # Main algorithm of this function,
    while my_queue and not timer.time_out():
        # get the next item off of the stack
        path = my_queue.next()

        # is if we happen to find a route around that entire matrix
        if len(path.tour) == len(edges):
            # if we find a route, we need to see if it's return trip is possible...
            best_score = score_tour(path.tour,edges)

            # if that return trip is still better, then we can add it as a best solution
            if best_score < BSSF:
                BSSF = best_score
                log.log_status(path.tour, best_score, timer.time(), my_queue.size(), nodes_extended, nodes_pruned, prune_tree)
            else:
                prune_tree.cut(path.tour)
                nodes_pruned += 1
            continue

        # for all nodes we have not visited
        for neighbor in set(range(len(edges))).difference(set(path.tour)):
            neighbor_matrix = path.matrix.reduced_cost_matrix(path.tour[-1], neighbor)
            new_score = path.score + edges[path.tour[-1]][neighbor]

            if neighbor_matrix.get_lower_bound() < BSSF and new_score < BSSF:
                new_tour = (path.tour.copy()) + [neighbor]
                nodes_extended += 1  # we have extended the node
                my_queue.push(new_tour,neighbor_matrix,new_score) # pushes the new score onto the stack
            else:
                prune_tree.cut(path.tour)
                nodes_pruned += 1

    return log.get_status_record()

