import random
from main import solveable

"""
generate_puzzles
------------------------------------
generates 100 puzzles of puzzles if given size 
------------------------------------
dimnesions - how big the puzzles generated should be
____________________________________
use: list = generate_puzzles(dimensions)
"""


def generate_puzzles(dimensions):
    puzzlelist = []
    if dimensions == 3:
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if dimensions == 4:
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    if dimensions == 5:
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]

    while len(puzzlelist) < 3:
        numbers = list(range(0, dimensions * dimensions))
        random.shuffle(numbers)
        if numbers not in puzzlelist and solveable(numbers, goal, dimensions):
            puzzlelist.append(numbers)
    return puzzlelist


generate_puzzles(3)
