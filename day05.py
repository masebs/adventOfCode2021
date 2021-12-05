# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

lines = []
with open("input-day05", 'r') as f:
# with open("input-day05-test", 'r') as f:
    lines = f.readlines()

# Read rules (save as list) and find maximum x and y coordinates
rules = []
maxX = 0
maxY = 0
for l in lines:
    l = l[:-1]
    l = l.split(' -> ')
    pointFrom = list(map(int, l[0].split(',')))
    pointTo   = list(map(int, l[1].split(',')))
    rules.append([pointFrom, pointTo])
    
    xmax = max([pointFrom[0], pointTo[0]])
    if xmax > maxX:
        maxX = xmax

    ymax = max([pointFrom[1], pointTo[1]])
    if ymax > maxY:
        maxY = ymax

# count active rules for each coordinate position (hand over empty grid to be modified)
def applyRules(grid, rules, ignoreDiagonal=False): 
    for r in rules:
        fromx, fromy = r[0]
        tox, toy = r[1]
        if fromy == toy: # horizontal line (could also be treated together with diagonals)
            if fromx > tox: # swap values if they are not in ascending order
                fromx, tox = tox, fromx
            for x in range(fromx, tox+1):
                grid[fromy][x] += 1
        elif fromx == tox: # vertical line (requires special treatment due to infinite slope)
            if fromy > toy: # swap values if they are not in ascending order
                fromy, toy = toy, fromy
            for y in range(fromy, toy+1):
                grid[y][fromx] += 1
        else:
            if not ignoreDiagonal:
                if fromx > tox: # swap values if they are not in ascending order
                    fromx, tox = tox, fromx
                    fromy, toy = toy, fromy # y elems must be swapped in the same way as x
                # slope = (tox-fromx) / (toy-fromy)
                slope = (toy-fromy) / (tox-fromx)
                if slope in [-1.0, 1.0]:
                    slope = int(slope)
                else:
                    print("WARNING: Invalid slope found:", slope)
                for k, x in enumerate(range(fromx, tox+1)):
                    grid[fromy+slope*k][x] += 1

# count values > threshold (threshold = 2 in this case)
def countLargeElems(grid, threshold):
    largeElems = [[el for el in grid[n] if el >= threshold] for n in range(len(grid))] # contains lists of the large elements in each line
    largeElems = [e for l in largeElems for e in l] # flatten the list to only contain the large elements
    return len(largeElems)

# Task 1
grid = [[0 for i in range(maxX+1)] for j in range(maxY+1)]
applyRules(grid, rules, ignoreDiagonal=True)
res = countLargeElems(grid, 2)
print(f"Task 1: Result is {res}")

# Task 2
grid = [[0 for i in range(maxX+1)] for j in range(maxY+1)]
applyRules(grid, rules, ignoreDiagonal=False)
res = countLargeElems(grid, 2)
print(f"Task 2: Result is {res}")

