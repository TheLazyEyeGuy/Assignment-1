"""
Main for the program, puzzles will be run through main and the program will rely on external
files in order to compile and solve the puzzles correctly
"""

# IMPORTS
from node import Node
from copy import copy
from queue import PriorityQueue

# CONSTANTS
HTYPE = 3

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
    closedQ = []
    count = 0
    steps = 0

    # Create node for start state
    startNode = Node(start, None, dim)
    startNode.g = 0
    calc_heuristic(startNode, goal, htype)
    startNode.f = startNode.g + startNode.h

    # Add startNode to from of open list
    openQ.put(startNode)
    closedQ.append(startNode.state)  # Add start node to visited states

    # Search Loop Until Open is empty
    while not openQ.empty():
        currentNode = openQ.get()  # Declare current as top of open queue
        count += 1
        # print(count)
        # Check if current node is the end state
        if currentNode.state == goal:
            # Do everything we need to do (return node count)
            # print("SOLUTION FOUND")
            # print_sol(copy(currentNode))
            while currentNode.parent != startNode:
                steps += 1
                currentNode = currentNode.parent

            return count, steps

        # Node not end node, expand open list with all neighbors, pass goal for h calculation
        n1, n2, n3, n4 = move_puzzle(closedQ, currentNode, goal,
                                     htype)  # Trys each movement and creates 4 nodes each whose parent is currentNode

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
    return 0, 0


"""
Prints solution (backwards)
"""


def print_sol(puzz):
    while puzz:
        puzz.print_state()
        print("")
        puzz = puzz.parent


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


def calc_heuristic(n, goal, htype):
    count = 0

    if htype == 1:
        # Counts # of states not in goal position, skips 0 position
        for i in range(len(goal)):
            if n.state[i] != 0 and n.state[i] != goal[i]:
                count += 1
        n.h = count

    elif htype == 2:
        # Calls function for each tile to sum distance from goal tile, adds to count
        count = manhattan_distance(n.state, goal, n.dim)
        n.h = count

    elif htype == 3:
        # Calls function to calculate linear conflicts + manhattan
        count = linear_conflicts(n.state, goal, n.dim)
        n.h = count

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
    for i in range(size * size):
        if s[i] != 0 and s[i] != goal[i]:
            gi = goal.index(s[i])
            total += abs((i // size) - (gi // size)) + abs(
                (i % size) - (gi % size))  # Calculates x and y values and heuristic

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
            i = (y * dim) + x
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
    if n.state in closedQ:
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
    fsize = size * size  # Flattened Size
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
    # Odd size
    if size % 2 != 0:
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
    # Even size
    else:
        loc = start.index(0)
        if loc // size % 2 == 0:
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
        else:
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


def move_puzzle(closedQ, n, goal, htype):
    x = n.index(0)

    left = move_left(closedQ, x, n, goal, htype)
    right = move_right(closedQ, x, n, goal, htype)
    up = move_up(closedQ, x, n, goal, htype)
    down = move_down(closedQ, x, n, goal, htype)

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


def move_left(closedQ, x, n, goal, htype):
    # will only be 0 if in position 0, n, 2n, ..., (n*n-n) (aka cant move left)
    if x % (n.dim) > 0:
        left = Node(copy(n.state), None, copy(n.dim))
        # Ye olde switch-a-roo
        temp = left.state[x - 1]
        left.state[x - 1] = left.state[x]
        left.state[x] = temp

        # Check if new state has already been visited
        # If not append left to visited nodes, if yes then return None
        if not visited(closedQ, left):
            closedQ.append(left.state)
            left.parent = n
            left.g = n.g + 1
            calc_heuristic(left, goal, htype)
            left.f = left.h + left.g
            return left
        else:
            del left
            return None
    return None


def move_right(closedQ, x, n, goal, htype):
    # Only enters if we can move right
    if x % (n.dim) < (n.dim - 1):

        right = Node(copy(n.state), None, copy(n.dim))
        # Ye olde switch-a-roo
        temp = right.state[x + 1]
        right.state[x + 1] = right.state[x]
        right.state[x] = temp

        # Check if new state has already been visited
        # If not append right to visited nodes, if yes then return None
        if not visited(closedQ, right):
            closedQ.append(right.state)
            right.parent = n
            right.g = n.g + 1
            calc_heuristic(right, goal, htype)
            right.f = right.h + right.g
            return right
        else:
            del right
            return None
    return None


def move_up(closedQ, x, n, goal, htype):
    if x - (n.dim) >= 0:
        up = Node(copy(n.state), None, copy(n.dim))
        # Ye olde switch-a-roo
        temp = up.state[x - (n.dim)]
        up.state[x - (n.dim)] = up.state[x]
        up.state[x] = temp

        # Check if new state has already been visited
        # If not append up to visited nodes, if yes then return None
        if not visited(closedQ, up):
            closedQ.append(up.state)
            up.parent = n
            up.g = n.g + 1
            calc_heuristic(up, goal, htype)
            up.f = up.h + up.g
            return up
        else:
            del up
            return None
    return None


def move_down(closedQ, x, n, goal, htype):
    if x + (n.dim) < (n.dim * n.dim):
        down = Node(copy(n.state), None, copy(n.dim))
        # Ye olde switch-a-roo
        temp = down.state[x + n.dim]
        down.state[x + n.dim] = down.state[x]
        down.state[x] = temp

        # Check if new state has already been visited
        # If not append down to visited nodes, if yes then return None
        if not visited(closedQ, down):
            closedQ.append(down.state)
            down.parent = n
            down.g = n.g + 1
            calc_heuristic(down, goal, htype)
            down.f = down.h + down.g
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


def solver(start, goal, dim):
    if not valid_state(start, dim) or not valid_state(goal, dim):
        print("Invalid start or end state")
        return

    # If puzzle can be solved all a_star to solve it
    if solveable(start, goal, dim):
        count = a_star(start, goal, dim)
        print("FINISHED ", count)
    else:
        print("There is no solution")


"""
Main
---------------------------------
Define a start and end state, test code
---------------------------------
"""

"""dim = 4
start = [1, 2, 4, 3, 6, 5, 8, 7, 9, 10, 13, 12, 11, 14, 15, 0]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]"""

"""dim = 3
start = [5, 6, 7, 4, 0, 8, 3, 2, 1]
goal = [1, 2, 3, 8, 0, 4, 7, 6, 5]


solver(start, goal, dim)"""
