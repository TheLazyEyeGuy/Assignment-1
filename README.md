# Assignment-1

from math import sqrt


class Puzzle:

    def __init__(self, numbers):
        self.list = numbers
        self.length = sqrt(len(numbers))
        self.validity = True  # function needed to determine state validity
        self.move_options = [True, True, True, True]  # cannot move until possible moves are determined

    def move_check(self):
        location = list.index(0)  # finds where in the puzzle the open spot is
        self.move_options = [True, True, True, True]

        if location <= (self.length - 1):
            self.move_options[0] = False
        if location % self.length == 0:
            self.move_options[1] = False
        if (location + 1) % self.length == 0:
            self.move_options[2] = False
        if (self.length * self.length)-1 >= location >= (self.length * self.length)-self.length:
            self.move_options[3] = False

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]

testing = Puzzle(list)
