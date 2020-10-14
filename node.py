"""
Class Node
Each Node represents a point on a graph, tree or list.
---------------------------------
self.state - state of puzzle node (3x3)
self.parent - points to the current nodes parent node
self.g - distance to starting node, used for heuristics
self.h - distance to goal node, used for heuristics
self.f - total cost node
------------------------------------------------------------------------------------
Three heuristics (self.h) possible:
h1) Hamming -> Number of tiles not in goalState (excludes 0)
h2) Manhattan -> Total amount of slides to reach goal state (Summed for each tile)
h3) Linear Conflict + Manhattan
    Tiles (a and b) are in linear conflict iff they are in the same row or column
    and the goal position of tile a is blocked by the current position of tile b
    Each linear conflict causes h to increase by 2
    h3 = h2 + 2*(# of Linear Conflicts)
"""


class Node:
    """
    Init each node upon call, edit these fields in external program to fit data structure
    """
    def __init__(self, state):
        self.UID = tuple(state)
        self.state = state #Uses array format
        self.g = 0 #Increases by 1 for each layer (= parent.g + 1)
        self.f = 0 # = g + h

    def __hash__(self):
        return hash(self.UID)

    """
    Comparator functions, take in self and other node for comparison
    Compares states for equality
    """
    def __eq__(self, other):
        for i in range(len(self.state)):
            if self.state[i] != other.state[i]:
                return False
        return True

    """
    Less than function, used for sorting lists/priority queue
    """
    def __lt__(self, other):
        if self.f < other.f:
            return True
        return False

    def __len__(self):
        return len(self.state)


    """
    Indexes self.state for the location of an item
    """
    def index(self, item):
        for i in range(len(self.state)):
            if self.state[i] == item:
                return i
        return None

