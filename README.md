from math import sqrt


class Puzzle:

    def __init__(self, numbers):
        """
        Description: constructor for puzzle class
        -------------------
        numbers = the raw puzzle data
        self.list = the puzzle represented in list format as a list
        self.length = the size of the puzzle ex.3x3, 4x4, 5x5, as an int such as 3,4,5
        self.validity = if this puzzle is valid/solvable as boolean
        self.move_options = what directions the 0 can move, goes in order UP LEFT RIGHT DOWN as list of 4 booleans
        ---------------------
        Example use: testing = Puzzle(numbers)
        """

        self.list = numbers
        self.length = sqrt(len(numbers))
        self.validity = True  # function needed to determine state validity
        self.move_options = [True, True, True, True]  # cannot move until possible moves are determined

    def move_check(self):
        """
        Description: calcualtes what directions the 0 can move in
        -------------------
        location = the index where the 0 resides
        self.move_options = what directions the 0 can move, goes in order UP LEFT RIGHT DOWN as list of 4 booleans
        ---------------------
        Example use: puzzle.move_check()
        """
        location = (self.list).index(0)  # finds where in the puzzle the open spot is
        self.move_options = [True, True, True, True]

        if location <= (self.length - 1):
            self.move_options[0] = False
        if location % self.length == 0:
            self.move_options[1] = False
        if (location + 1) % self.length == 0:
            self.move_options[2] = False
        if (self.length * self.length) - 1 >= location >= (self.length * self.length) - self.length:
            self.move_options[3] = False

        print(self.move_options)


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]

testing = Puzzle(numbers)
testing.move_check()
testing.list = [0, 2, 3, 4, 5, 6, 7, 8, 1]
testing.move_check()
