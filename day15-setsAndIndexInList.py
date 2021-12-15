# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

### Improved: Using sets for both green and yellow (to speed up "in" ops), still managing yellows in a list
###           sorting it every step, but now not using the objects itself in the list and sets, but only
###           tupels containing distance and index. Saves around 3 s compared to storing object, runs 15 s

import numpy as np

with open("input-day15", 'r') as f:
# with open("input-day15-test", 'r') as f:
    grid = [[int(i) for i in c] for l in f.readlines() for c in l.split() ]
nrows = len(grid)
ncols = len(grid[0])

npgrid = np.array(grid)
ngrids = 5

def incrementGrid(grid, inc):
    incGrid = grid.copy()
    for _ in range(inc):
        incGrid += 1
        incGrid[np.where(incGrid == 10)] = 1
    return incGrid
    
largegrid = np.zeros((5*nrows, 5*ncols), dtype=int)
for x in range(ngrids):
    for y in range(ngrids):
        largegrid[x*nrows:(x+1)*nrows, y*ncols:(y+1)*ncols] = incrementGrid(npgrid, x+y)

class Node:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.dist  = 9e9
        self.prev  = None

def getNeighborIndices(n, bounds):
    nbs = []
    i,j = n.index
    idcs = [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]
    for idx in idcs:
        if 0 <= idx[0] < bounds[0] and 0 <= idx[1] < bounds[1]:
            nbs.append(idx)
    return nbs

def dijkstra(grid, startidx, endidx):
    yellow = []
    yellowSet = set() # using additional Set for more efficient "in" (contains) op saves ~3s
    green  = set() # using set instead of list for green: 26 s w/o, 45 s with output instead of > 10 min with list
    ngrid = []
    for i, r in enumerate(grid):
        ngridrow = []
        for j, c in enumerate(r):
            n = Node((i,j), c)
            ngridrow.append(n)
        ngrid.append(ngridrow)
            
    start = ngrid[startidx[0]][startidx[1]]
    start.dist = 0 # set source distance
    end   = ngrid[endidx[0]][endidx[1]]
    yellow.append((start.dist, start.index)) # using tupels in list instead of the object itself
    yellowSet.add(start.index)
    
    while yellow:
        yellow.sort(key = lambda el: el[0], reverse=True)   
        x, y = yellow.pop()[1]
        n = ngrid[x][y]
        green.add(n.index)
        # print(f" setting green: idx {n.index}, len(green): {len(green)}, len(yellow): {len(yellow)}")
        if n == end:
            return end
        nbs = [ngrid[idx[0]][idx[1]] for idx in getNeighborIndices(n, grid.shape)]
        for nbr in nbs:
            if nbr.index not in green and nbr.index not in yellowSet:
                nbr.prev = n
                nbr.dist = n.dist + nbr.value
                yellow.append((nbr.dist, nbr.index))
                yellowSet.add(nbr.index)
            elif nbr in yellowSet:
                if nbr.dist > n.dist + nbr.value:
                    nbr.prev = n
                    nbr.dist = n.dist + nbr.value
    
end = dijkstra(npgrid, (0,0), (nrows-1, ncols-1))
print(f"Task 1: Easiest path has weight {end.dist}")

end = dijkstra(largegrid, (0,0), (ngrids*nrows-1, ngrids*ncols-1))
print(f"Task 2: Easiest path has weight {end.dist}")
    