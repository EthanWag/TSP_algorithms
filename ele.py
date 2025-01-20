class ele:
    def __init__(self,tour,matrix,score):
        self.tour = tour
        self.matrix = matrix
        self.score = score

    def __lt__(self, other):
        return self.score < other.score