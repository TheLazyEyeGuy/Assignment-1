"""
Main for the program, puzzles will be run through main and the program will rely on external
files in order to compile and solve the puzzles correctly
"""


# IMPORTS
from node import Node
from copy import copy
from queue import PriorityQueue
from collections import deque
from math import inf

"""
a_star
---------------
Uses heuristics to search for the solution to a slide puzzle
---------------
start - The root/starting state in the tree (dim x dim matrix)
end - The goal state aka: the puzzles complete state (dim x dim matrix)
dim - size of puzzle matrix (dim x dim)
---------------
nodes_visited - Returns the number of nodes visited for output (int)
---------------
use example: self.a_star(tree, startState, endState);
"""
def a_star(start, goal, dim, htype):
    # Lists for open and closed nodes
    openQ = PriorityQueue()
    # List for visited states
    closedQ = {}
    count = 0

    # Create node for start state
    startNode = Node(start)
    startNode.g = 0
    calc_heuristic(startNode, goal, dim, htype)
    startNode.f += startNode.g

    # Add startNode to from of open list
    openQ.put(startNode)
    closedQ[startNode.UID] = True   # Add start node to visited states

    # Search Loop Until Open is empty
    while not openQ.empty():
        currentNode = openQ.get()  # Declare current as top of open queue
        count += 1
        # Check if current node is the end state
        if currentNode.state == goal:
            # Do everything we need to do (return node count)
            return currentNode.g, count

        # Node not end node, expand open list with all neighbors, pass goal for h calculation
        n1, n2, n3, n4 = move_puzzle(closedQ, currentNode, goal, dim, htype) #Trys each movement and creates 4 nodes each whose parent is currentNode

        # Appends nodes to list only if they are not None
        if n1:
            openQ.put(n1)
        if n2:
            openQ.put(n2)
        if n3:
            openQ.put(n3)
        if n4:
            openQ.put(n4)

    # This return is only used if no solution found, should never be called
    return count


"""
ida_star
--------------------------------------------------
A* But uses f heuristic of start state as a cut off
for the openQ. Slower than A* but significantly more
efficient for memory. Works recursively
--------------------------------------------------
start - array for start state
goal - array for goal state
dim - dimensions for puzzles (8 puzzle - 3x3 - dim = 3)
--------------------------------------------------
length of openQ - 1: Equal to # of steps taken to solve puzzle
count - The number for nodes expanded searching for the solution
--------------------------------------------------
use example: steps, expanded = ida_star(start, goal, dim)
"""
def ida_star(start, goal, dim, htype):

    """
    search
    -------------------------------------------
    Recursive alg to perform IDA*, returns if f > threshold
    or if the goal is reached. If f is returned the threshold will
    be updated to f to avoid dead ends in the algorithm
    -------------------------------------------
    openQ - deque used for holding states
    g - the g heuristic of the parent node
    threshold - the current max f heuristic value that is allowed to be expanded
    count - The current total number of nodes expanded
    -------------------------------------------
    multi use - can return inf, a new max f, or a boolean
        returns inf if unsolvable, f to increase threshold
        and boolean if the goal state has been found
    count - the total number of nodes expanded
    -------------------------------------------
    eg use: a, b = search(openQ, 0, threshold, count)
    """
    def search(currentNode, goal, threshold, count, dim, htype):
        count += 1
        if currentNode.f > threshold:  # Used to update min
            return currentNode.f, count, currentNode.g
        if currentNode.state == goal:  # If goal reached return
            return True, count, currentNode.g
        minF = inf
        poss = possible_moves(currentNode, closedQ, goal, dim, htype)
        for i in poss: #Only items not in closed Q can be in poss
            closedQ[i.UID] = True #Add Node to closedQ
            t, count, steps = search(i, goal, threshold, count, dim, htype)
            if t is True:
                return True, count, steps
            if t < minF:  # If currentNode.f of last recurse < min, update min
                minF = t

        return minF, count, currentNode.g  # Return min to update new threshold



    # Create node for start state
    startNode = Node(start)
    startNode.g = 0
    calc_heuristic(startNode, goal, dim, htype)
    startNode.f += startNode.g
    count = 0

    threshold = startNode.f
    # Search Loop Until Open is empty
    while True:
        closedQ = {startNode.UID: True}
        t, count, depth = search(startNode, goal, threshold, count, dim, htype)

        if t is True:  # Solution found
            return depth, count
        elif t == inf:  # Should never happen, unsolveable cases should be caught by solveable, here just incase
            return depth, count

        threshold = t  # Cannot find solution with prev threshold, update to smallest f found, search again



"""
possible_moves
---------------------------------------------------
Gets a list of possible puzzle states given a beginning states
Similar to move_puzzle but returns a 2d array containing the possible
new states (repped as arrays), does not use Node datatype
---------------------------------------------------
node - beginning state (array len dim x dim)
dim - dimensions of puzzle
---------------------------------------------------
poss - list of possible move states (each length dim x dim, max 4 arrays)
---------------------------------------------------
use eg: moveList = possible_moves(start, dim)
"""
def possible_moves(node, closedQ, goal, dim, htype):
    poss = []
    x = node.index(0)
    if x % dim > 0:
        left = copy(node.state)  # Could make swap function for better readability
        temp = left[x - 1]
        left[x - 1] = left[x]
        left[x] = temp
        left = Node(left)

        if not visited(closedQ, left): #Check if Node is closed, if not calc heuristics
            left.g = node.g + 1
            calc_heuristic(left, goal, dim, htype)
            left.f += left.g
            poss.append(left)
        else: #If node is closed delete node
            del left
    if x % dim + 1 < dim:
        right = copy(node.state)
        temp = right[x + 1]
        right[x + 1] = right[x]
        right[x] = temp
        right = Node(right)

        if not visited(closedQ, right):
            right.g = node.g + 1
            calc_heuristic(right, goal, dim, htype)
            right.f += right.g
            poss.append(right)
        else:
            del right
    if x - dim >= 0:
        up = copy(node.state)
        temp = up[x - dim]
        up[x - dim] = up[x]
        up[x] = temp
        up = Node(up)

        if not visited(closedQ, up):
            up.g = node.g + 1
            calc_heuristic(up, goal, dim, htype)
            up.f += up.g
            poss.append(up)
        else:
            del up
    if x + dim < len(node):
        down = copy(node.state)
        temp = down[x + dim]
        down[x + dim] = down[x]
        down[x] = temp
        down = Node(down)

        if not visited(closedQ, down):
            down.g = node.g + 1
            calc_heuristic(down, goal, dim, htype)
            down.f += down.g
            poss.append(down)
        else:
            del down

    return poss


"""
calc_heuristic
-----------------------------------------------
Calculates state.h using one of three types of heuristics
-----------------------------------------------
n - Node to calculate heuristic for (Node)
start - Start state of puzzle (array)
goal - Goal state of puzzle (array)
htype - type of heuristic (1 - Hamming, 2 - Manhattan, 3 - Linear Conflict)
-----------------------------------------------
returns nothing, sets n.h = ?
-----------------------------------------------
example use:
calc_heuristics(left, start, goal, 1) - Calcs Hamming heuristic and stores value in left.h
-----------------------------------------------
h1) Hamming -> Number of tiles not in goalState (excludes 0)
h2) Manhattan -> Total amount of slides to reach goal state (Summed for each tile)
h3) Linear Conflict + Manhattan
    Tiles (a and b) are in linear conflict iff they are in the same row or column
    and the goal position of tile a is blocked by the current position of tile b
    Each linear conflict causes h to increase by 2
    h3 = h2 + 2*(# of Linear Conflicts)
"""
def calc_heuristic(n, goal, dim, htype):
    count = 0

    if htype == 1:
        # Counts # of states not in goal position, skips 0 position
        for i in range(dim*dim):
            if n.state[i] != 0 and n.state[i] != goal[i]:
                count += 1
        n.f = count

    elif htype == 2:
        # Calls function for each tile to sum distance from goal tile, adds to count
        count = manhattan_distance(n.state, goal, dim)
        n.f = count

    elif htype == 3:
        # Calls function to calculate linear conflicts + manhattan
        count = linear_conflicts(n.state, goal, dim)
        n.f = count

    else:
        print("INVALID TYPE, NOTHING SET")


"""
manhattan_distance
----------------------------------------
Calculates the number of slides each tile needs to do
to reach their goal state from state n
----------------------------------------
s - State of the puzzle
goal - goal state of puzzle
size - size of one column/row (total size is size x size)
----------------------------------------
returns total number of slides
----------------------------------------
eg use:
count = manhattan_distance(n.state, goal)
"""
def manhattan_distance(s, goal, size):
    total = 0
    for i in range(size*size):
        if s[i] != 0 and s[i] != goal[i]:
            gi = goal.index(s[i])
            total += abs((i//size) - (gi//size)) + abs((i%size) - (gi%size)) #Calculates x and y values and heuristic

    return total


"""
linear_conflicts
----------------------------------------
Calculates the number of linear conflicts between
a given state (s) and a goal state
----------------------------------------
s - Given state (s)
goal - goal state of puzzle
size - dimensions of puzzle (size x size)
----------------------------------------
returns total number of conflicts
----------------------------------------
eg use:
count = linear_conflicts(n.state, goal)
"""
def linear_conflicts(s, goal, dim):
    """
    conflict_count
    -------------------------------------
    Nested function for counting conflicts in a row/column
    -------------------------------------
    s_row - row in s
    goal_row - row in goal
    size - dimension of matrix (size x size)
    -------------------------------------
    returns count - count of conflicts in given row
    -------------------------------------
    eg use:
    count += conflict_count(s_row, goal_row, size)
    """
    def conflict_count(s_row, goal_row, size, t=0):
        count = [0 for x in range(size)]
        for j, t1 in enumerate(s_row):
            if t1 in goal_row and t1 != 0:
                for k, t2 in enumerate(s_row):
                    if t2 in goal_row and t2 != 0 and t1 != t2:
                        if (goal_row.index(t1) > goal_row.index(t2)) and j < k:
                            count[j] += 1
                        if (goal_row.index(t1) < goal_row.index(t2)) and j > k:
                            count[j] += 1
        if max(count) == 0:
            return t * 2
        else:
            j = count.index(max(count))
            s_row[j] = -1
            t += 1
            return conflict_count(s_row, goal_row, size, t)

    total = manhattan_distance(s, goal, dim)

    s_rows = [[] for y in range(dim)]
    s_cols = [[] for x in range(dim)]
    goal_rows = [[] for y in range(dim)]
    goal_cols = [[] for x in range(dim)]
    for y in range(dim):
        for x in range(dim):
            i = (y*dim) + x
            s_rows[y].append(s[i])
            s_cols[x].append(s[i])
            goal_rows[y].append(goal[i])
            goal_cols[x].append(goal[i])
    for i in range(dim):
        total += conflict_count(s_rows[i], goal_rows[i], dim)
    for i in range(dim):
        total += conflict_count(s_cols[i], goal_cols[i], dim)
    return total


"""
visited
--------------------------
Function to check if a node has been visited or not
--------------------------
closed - list of nodes that have been visited (array[Node])
n - Node/puzzle state that we are checking (Node)
--------------------------
returns true if visited, false if not_visited
--------------------------
example use:
if visited(closed, moveLeft): Add node to open queue else: Don't
    ^Checks if moving left from curr has been done, if not add to queue
"""
def visited(closedQ, n):
    if closedQ.get(n.UID):
        return True
    return False


"""
valid_state
-------------------------------------
Checks if the state of a puzzle is valid
-------------------------------------
s - state to check validity of
size - number of dimensions in 2d array (size x size)
-------------------------------------
returns true if valid, false if not valid
-------------------------------------
example use:
if valid_state(s): do something else: don't
"""
def valid_state(s, size):
    i = 0
    fsize = size*size  # Flattened Size
    if len(s) != fsize:
        return False  # HAPPENS IF GIVING 3x3 WITH DIM = 4
    # Loop checks if numbers are all in proper range 0-(fsize-1)
    for i in range(fsize):
        if s[i] > (fsize - 1) or s[i] < 0:
            return False
    valid = [0 for i in range(fsize)]  # All numbers in list valid, use this to confirm
    # Loop to check if there are repeat numbers (2 of any number is invalid)
    for i in range(fsize):
        if valid[s[i]] == 0:
            valid[s[i]] = 1
        else:
            return False
    return True


"""
solveable
----------------------------------------
Checks if a given goal state is reachable from a given start state
Counts inversions, if number of inversions is even than the puzzle is solveable
----------------------------------------
start - Beginning state of puzzle (Array)
goal - End/Goal state of puzzle (Array)
size - Dimensions of puzzle (size x size)
----------------------------------------
returns True if reachable, False if not
----------------------------------------
example use:
if solveable(startNode, goalNode): solve_puzzle else: exit
"""
def solveable(start, goal, size):
    if not (valid_state(start, size) and valid_state(goal, size)):
        return False  # Either the start or end state is invalid
    # Odd size dimension (3x3, 5x5)
    # This requires inversions to be even for solveable
    if size % 2 != 0:
        fsize = size*size # Flattened size dimension
        count = 0
        # Loop i for anchor, compares i with all other positions infront of it (j)
        for i in range(fsize):
            # Loop j for moving comparator, always ahead of i by 1 more more spaces
            for j in range(i+1, fsize):
                if start[i] and start[j] and start[i] > start[j]:
                    count += 1  # If both states valid and i > j there is an inversion, add 1 to count
                if goal[i] and goal[j] and goal[i] > goal[j]:
                    count += 1

        # Count % 2 is 0 if even, even returns True
        if count % 2 == 0:
            return True

        return False
    # Even size dimension (4x4, 6x6)
    else:
        loc = start.index(0)
        if loc//size % 2 == 0:  # 0 starts in an EVEN row (0, 2, 4) requires ODD inversions
            fsize = size * size  # Flattened size dimension
            count = 0
            # Loop i for anchor, compares i with all other positions infront of it (j)
            for i in range(fsize):
                # Loop j for moving comparator, always ahead of i by 1 more more spaces
                for j in range(i + 1, fsize):
                    if start[i] and start[j] and start[i] > start[j]:
                        count += 1  # If both states valid and i > j there is an inversion, add 1 to count
                    if goal[i] and goal[j] and goal[i] > goal[j]:
                        count += 1

            # Count % 2 is 0 if even, even returns True
            if count % 2 != 0:
                return True

            return False
        else:  # 0 starts in an ODD row (1, 3, 5), requires EVEN inversions
            fsize = size * size  # Flattened size dimension
            count = 0
            # Loop i for anchor, compares i with all other positions infront of it (j)
            for i in range(fsize):
                # Loop j for moving comparator, always ahead of i by 1 more more spaces
                for j in range(i + 1, fsize):
                    if start[i] and start[j] and start[i] > start[j]:
                        count += 1  # If both states valid and i > j there is an inversion, add 1 to count
                    if goal[i] and goal[j] and goal[i] > goal[j]:
                        count += 1

            # Count % 2 is 0 if even, even returns True
            if count % 2 == 0:
                return True

            return False

"""
move_puzzle
------------------------------------
Moves the 0 position up, left, right, and down
creates new node with n as parent node for each move
only creates new node if it has not existed previously
------------------------------------
closedQ - List of already visited nodes
n - node containing current state of puzzle
goal - goal state of puzzle for heuristics
"""
def move_puzzle(closedQ, n, goal, dim, htype):
    x = n.index(0)

    left = move_left(closedQ, x, n, goal, dim, htype)
    right = move_right(closedQ, x, n, goal, dim, htype)
    up = move_up(closedQ, x, n, goal, dim, htype)
    down = move_down(closedQ, x, n, goal, dim, htype)

    return left, right, up, down


"""
Description for 4 functions:
    move_left, right, up, down
-----------------------------------------
below functions move 0 in puzzle up left right and down
these nodes are assigned n as a parent, state maybe NULL
-----------------------------------------
closedQ - List containing previously visited nodes
x - location of 0 in n
n - Node containing current state of puzzle
goal - goal state of puzzle for heuristics
------------------------------------------
eg use:
move_left(closedQ, x, n)
"""
def move_left(closedQ, x, n, goal, dim, htype):
    # will only be 0 if in position 0, n, 2n, ..., (n*n-n) (aka cant move left)
    if x%dim > 0:
        left = copy(n.state)
        temp = left[x-1]
        left[x-1] = left[x]
        left[x] = temp
        left = Node(left)

        # Check if new state has already been visited
        # If not append left to visited nodes, if yes then return None
        if not visited(closedQ, left):
            closedQ[left.UID] = True
            left.g = n.g + 1
            calc_heuristic(left, goal, dim, htype)
            left.f = left.f + left.g
            return left
        else:
            del left
            return None
    return None


def move_right(closedQ, x, n, goal, dim, htype):
    # Only enters if we can move right
    if x%dim < (dim-1):
        right = copy(n.state)
        temp = right[x+1]
        right[x+1] = right[x]
        right[x] = temp
        right = Node(right)

        # Check if new state has already been visited
        # If not append right to visited nodes, if yes then return None
        if not visited(closedQ, right):
            closedQ[right.UID] = True
            right.g = n.g + 1
            calc_heuristic(right, goal, dim, htype)
            right.f = right.f + right.g
            return right
        else:
            del right
            return None
    return None


def move_up(closedQ, x, n, goal, dim, htype):
    if x-dim >= 0:
        up = copy(n.state)
        temp = up[x-dim]
        up[x-dim] = up[x]
        up[x] = temp
        up = Node(up)

        # Check if new state has already been visited
        # If not append up to visited nodes, if yes then return None
        if not visited(closedQ, up):
            closedQ[up.UID] = True
            up.g = n.g + 1
            calc_heuristic(up, goal, dim, htype)
            up.f = up.f + up.g
            return up
        else:
            del up
            return None
    return None


def move_down(closedQ, x, n, goal, dim, htype):
    if x+dim < (dim*dim):
        down = copy(n.state)
        temp = down[x+dim]
        down[x+dim] = down[x]
        down[x] = temp
        down = Node(down)

        # Check if new state has already been visited
        # If not append down to visited nodes, if yes then return None
        if not visited(closedQ, down):
            closedQ[down.UID] = True
            down.g = n.g + 1
            calc_heuristic(down, goal, dim, htype)
            down.f = down.f + down.g
            return down
        else:
            del down
            return None
    return None


"""
solver
-------------------------------------------
given a start and end state solves the puzzle if possible
-------------------------------------------
start - start state of puzzle
goal - goal state of puzzle
dim - puzzle dimensions (dim x dim)
-------------------------------------------
returns nothing
-------------------------------------------
example use:
solver(start, end)
"""
"""def solver(start, goal, dim, htype):
    if not valid_state(start, dim) or not valid_state(goal, dim):
        print("Invalid start or end state")
        return

    #If puzzle can be solved all a_star to solve it
    if solveable(start, goal, dim):
        #steps, count = a_star(start, goal, dim, htype)
        steps, count = ida_star(start, goal, dim, htype)
        print("STEPS: ", steps, " NODES EXPANDED: ", count)
    else:
        print("There is no solution")"""

"""
Main
---------------------------------
Define a start and end state, test code
---------------------------------
"""

"""dim = 4
start = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 0]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]"""

"""dim = 3
start = [8, 6, 7, 2, 5, 4, 3, 0, 1]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]"""

"""dim = 5
start = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 21, 14, 15, 16, 17, 0, 19, 20, 13, 22, 23, 24, 18]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]"""


"""solver(start, goal, dim, 3)"""