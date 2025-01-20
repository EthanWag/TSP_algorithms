import math

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree
from record import Record

def find_greedy(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    log = Record()
    nodes_expanded = 0

    # This is just in case we get stuck in corners, we at least end at some point
    for start in range(len(edges)):
        node = start
        edge_set = set()

        tour = []
        score = 0

        # gets everything but the last edge
        while node not in edge_set:
            if timer.time_out(): return log.get_status_record()

            tour.append(node)
            edge_set.add(node)
            row = edges[node]

            # if this is the final edge, then we need to back to get the final loop
            if len(edge_set) == len(edges):
                edge_set.remove(start)

            min_score, min_index = min((score, idx) for idx, score in enumerate(row) if idx not in edge_set)

            # checks to see if we have found
            if min_score is not math.inf:
                edge_set.add(start) # Always puts the edge back in it's place
                node = min_index
                score += min_score
                nodes_expanded += 1

        if len(edge_set) == len(edges) and score < math.inf:
            log.log_status(tour, score, timer.time(), 0, nodes_expanded, 0, CutTree(len(edges)))
            break

    return log.get_status_record()









'''

recorder = Record() # this will just record the status of the greedy tour

    # just in case we don't find an optimal solution
    for start in range(len(edges)):

        node = start
        edge_set = set()

        tour = []
        score = 0

        while node not in edge_set:

            edge_set.add(node)
            tour.append(node)

            # just gets the row and keeps things clean
            row = edges[node]
            min_score = math.inf
            min_index = None

            for neighbor in range(len(row)):
                if row[neighbor] < min_score and neighbor not in edge_set:
                    min_index = neighbor
                    min_score = row[neighbor]

            # if anything changed at all, we do something about it
            if min_index is not None:
                node = min_index
                score += min_score
                
        # need to account for the fact that we actually need to include the route back to the start

        # if the length of our set is equal to the length of the edges, then we have found a tour
        if len(edge_set) == len(edges):
            break

'''

