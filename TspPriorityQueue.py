import heapq as heapq
import math as math
from ele import ele

class TspPriorityQueue:

    def __init__(self, total_size:int):
        self.heap = []
        self.graph_size = total_size

    def push(self, tour, matrix, score):
        new_ele = ele(tour, matrix, score)
        heapq.heappush(self.heap, (self.graph_size - len(new_ele.tour), new_ele))

    def next(self):
        return heapq.heappop(self.heap)[1]

    def size(self):
        return len(self.heap)

    def __bool__(self):
        return len(self.heap) > 0

