import main
from generate import generate_puzzles

threelist = generate_puzzles(3)
fourlist = generate_puzzles(4)
fivelist = generate_puzzles(5)

threegoal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
fourgoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
fivegoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]

print("3*3")
nodecount = nodeh1 = nodeh2 = nodeh3 = stepscount = stepsh1 = stepsh2 = stepsh3 = 0
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
for i in threelist:
    nodecount, stepscount = main.a_star(i, threegoal, 3, 1)
    nodeh1 += nodecount
    stepsh1 += stepscount
    nodecount, stepscount = main.a_star(i, threegoal, 3, 2)
    nodeh2 += nodecount
    stepsh2 += stepscount
    nodecount, stepscount = main.a_star(i, threegoal, 3, 3)
    nodeh3 += nodecount
    stepsh3 += stepscount
print("amount of nodes for h1: ", nodeh1, ", amount of steps for h1: ", stepsh1)
print("amount of nodes for h2: ", nodeh2, ", amount of steps for h2: ", stepsh2)
print("amount of nodes for h3: ", nodeh3, ", amount of steps for h3: ", stepsh3)
"""
print("")
print("4*4")
nodecount = nodeh1 = nodeh2 = nodeh3 = stepscount = stepsh1 = stepsh2 = stepsh3 = 0
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
for i in fourlist:
    nodecount, stepscount = main.a_star(i, fourgoal, 3, 1)
    nodeh1 += nodecount
    stepsh1 += stepscount
    nodecount, stepscount = main.a_star(i, fourgoal, 3, 2)
    nodeh2 += nodecount
    stepsh2 += stepscount
    nodecount, stepscount = main.a_star(i, fourgoal, 3, 3)
    nodeh3 += nodecount
    stepsh3 += stepscount
print("amount of nodes for h1: ", nodeh1, ", amount of steps for h1: ", stepsh1)
print("amount of nodes for h2: ", nodeh2, ", amount of steps for h2: ", stepsh2)
print("amount of nodes for h3: ", nodeh3, ", amount of steps for h3: ", stepsh3)
print("")
print("5*5")
nodecount = nodeh1 = nodeh2 = nodeh3 = stepscount = stepsh1 = stepsh2 = stepsh3 = 0
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
for i in fivelist:
    nodecount, stepscount = main.a_star(i, fivegoal, 3, 1)
    nodeh1 += nodecount
    stepsh1 += stepscount
    nodecount, stepscount = main.a_star(i, fivegoal, 3, 2)
    nodeh2 += nodecount
    stepsh2 += stepscount
    nodecount, stepscount = main.a_star(i, fivegoal, 3, 3)
    nodeh3 += nodecount
    stepsh3 += stepscount
print("amount of nodes for h1: ", nodeh1, ", amount of steps for h1: ", stepsh1)
print("amount of nodes for h2: ", nodeh2, ", amount of steps for h2: ", stepsh2)
print("amount of nodes for h3: ", nodeh3, ", amount of steps for h3: ", stepsh3)
"""