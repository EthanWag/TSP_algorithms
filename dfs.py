import math

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from record import Record
from tsp_cuttree import CutTree


def find_dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    solver = Private_Dfs(timer,edges)

    # maybe put this inside of a loop so you can get all the possible solutions
    for start in range (len(edges)): # O(1) we never even get here
        if timer.time_out(): # just makes sure we do not time out
            return solver.results()
        tour = []
        score = 0
        solver.dfs(tour,score,start)

    return [solver.results()[-1]] # returns the last solution, if you want more, just uncomment the lists stuff

# A class to keep track of the stats
class Private_Dfs:

    def __init__(self, timer:Timer,edges: list[list[float]]):
     # record stuff
     self.nodes_expanded = 0
     self.log = Record()
     self.timer = timer

     # stuff for keeping track of the best solution
     self.edges = edges
     self.BSSF = math.inf

    def results(self):
        return self.log.get_status_record()

    # Main dfs Algorithm
    def dfs(self,tour,score,node): #

        if self.timer.time_out():
            return # timed out, finish

        tour.append(node) # just adds the node to our tour

        if len(tour) == len(self.edges):
            score += self.edges[node][tour[0]] # can we make a return trip?

            if score < self.BSSF:
                self.BSSF = score
                self.log.log_status(tour,score,self.timer.time(),0,self.nodes_expanded,0,CutTree(len(self.edges)))

            return # we are done with the branch

        row = self.edges[node]

        # visits each of the possibilities for the next node
        for neighbor in range(len(row)):
            if neighbor not in tour and row[neighbor] != math.inf:
                new_score = score + row[neighbor]
                self.nodes_expanded += 1  # we have now expanded to a new node
                self.dfs(tour.copy(),new_score,neighbor)
