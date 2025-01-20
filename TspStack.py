from ele import ele

class TspStack:

    # you pass in it's initial values
    def __init__(self):
        self.stack = []

    def push(self, tour,matrix,score):
        new_ele = ele(tour,matrix,score)
        self.stack.append(new_ele) # pushes a new item onto the stack

    def pop(self):
        return self.stack.pop()

    def next(self):
        return self.pop()

    def size(self):
        return len(self.stack)

    def __bool__(self):
        return len(self.stack) > 0