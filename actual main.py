import main
from generate import generate_puzzles

threelist = generate_puzzles(3)
fourlist = generate_puzzles(4)
fivelist = generate_puzzles(5)

threegoal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
fourgoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
fivegoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]

print("4*4 - Hamming")
nodecount = nodetotal = stepscount = stepstotal = 0
puzzlenumber = 1
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
print("Puzzle Number     Nodes Expanded     Steps Taken            Puzzle")
print("---------------------------------------------------------------------------")
for i in fourlist:
    nodecount, stepscount = main.a_star(i, fourgoal, 4, 1)
    print(str(puzzlenumber).ljust(18), str(nodecount).rjust(13), str(stepscount).rjust(15), "  ", str(i).ljust(40))
    nodetotal += nodecount
    stepstotal += stepscount
    puzzlenumber += 1

print("total nodes for Hamming: ", nodetotal, ", total steps for Hamming: ", stepstotal)
#(1 - Hamming, 2 - Manhattan, 3 - Linear Conflict)
print("---------------------------------------------------------------------------")
print("4*4 - Manhattan")
nodecount = nodetotal = stepscount = stepstotal = 0
puzzlenumber = 1
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
print("Puzzle Number     Nodes Expanded     Steps Taken            Puzzle")
print("---------------------------------------------------------------------------")
for i in fourlist:
    nodecount, stepscount = main.a_star(i, fourgoal, 4, 2)
    print(str(puzzlenumber).ljust(18), str(nodecount).rjust(13), str(stepscount).rjust(15), "  ", str(i).ljust(40))
    nodetotal += nodecount
    stepstotal += stepscount
    puzzlenumber += 1

print("total nodes for Manhattan: ", nodetotal, ", total steps for Manhattan: ", stepstotal)
#(1 - Hamming, 2 - Manhattan, 3 - Linear Conflict)
print("---------------------------------------------------------------------------")
print("4*4 - Linear Conflict")
nodecount = nodetotal = stepscount = stepstotal = 0
puzzlenumber = 1
#this for loop runs every puzzle using all heuristics and adds up the total node and step costs
print("Puzzle Number     Nodes Expanded     Steps Taken            Puzzle")
print("---------------------------------------------------------------------------")
for i in fourlist:
    nodecount, stepscount = main.a_star(i, fourgoal, 4, 3)
    print(str(puzzlenumber).ljust(18), str(nodecount).rjust(13), str(stepscount).rjust(15), "  ", str(i).ljust(40))
    nodetotal += nodecount
    stepstotal += stepscount
    puzzlenumber += 1

print("total nodes for Linear Conflict: ", nodetotal, ", total steps for Linear Conflict: ", stepstotal)
#(1 - Hamming, 2 - Manhattan, 3 - Linear Conflict)
print("---------------------------------------------------------------------------")