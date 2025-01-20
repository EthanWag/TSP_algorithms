from tsp_core import SolutionStats


class Record:

    def __init__(self):
        self.status_log = [] # just a list of all the solutions

    def log_status(self, tour, cost:float, time:float, queue_size:int, n_nodes_expanded:int, n_nodes_pruned:int, cut_tree):
        self.status_log.append(SolutionStats(
            tour=tour,
            score=cost,
            time=time,
            max_queue_size=queue_size,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    def get_status_record(self):
        return self.status_log