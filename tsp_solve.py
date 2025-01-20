import math
import random

from tsp_core import SolutionStats, Timer, score_tour
from tsp_cuttree import CutTree

import greedy as greedy
import dfs as my_dfs
import branch_bound as bnb

from TspStack import TspStack
from TspPriorityQueue import TspPriorityQueue as pq



def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = [] # setting up basics, nothing to really do with the code below
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out(): # main timer, if we run out of time, we return what stats we have
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats( # if we find a solution, we log it. Do we log it at the end or during the process
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return greedy.find_greedy(edges, timer)


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return my_dfs.find_dfs(edges, timer)


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return bnb.find_branch_bound(edges, timer,TspStack(),0)

def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return bnb.find_branch_bound(edges,timer,pq(len(edges)),0)
