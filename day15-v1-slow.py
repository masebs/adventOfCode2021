# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

### The original version, using Dijkstra with all lists. Runs very long (more than 5 min at least)

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
    green  = []
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
    yellow.append(start)
    
    while yellow:
        yellow.sort(key = lambda node: node.dist, reverse=True)    
        n = yellow.pop()
        green.append(n)
        print(f" setting green: idx {n.index}, len(green): {len(green)}, len(yellow): {len(yellow)}")
        if n == end:
            return end
        nbs = [ngrid[idx[0]][idx[1]] for idx in getNeighborIndices(n, grid.shape)]
        for nbr in nbs:
            if nbr not in green and nbr not in yellow:
                nbr.prev = n
                nbr.dist = n.dist + nbr.value
                yellow.append(nbr)
            elif nbr in yellow:
                if nbr.dist > n.dist + nbr.value:
                    nbr.prev = n
                    nbr.dist = n.dist + nbr.value
    
end = dijkstra(npgrid, (0,0), (nrows-1, ncols-1))
print(f"Task 1: Easiest path has weight {end.dist}")

end = dijkstra(largegrid, (0,0), (ngrids*nrows-1, ngrids*ncols-1))
print(f"Task 2: Easiest path has weight {end.dist}")
    