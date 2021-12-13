# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

with open("input-day13", 'r') as f:
# with open("input-day13-test", 'r') as f:
    lines = [l.split() for l in f.readlines()]

points = []
folds  = []

for l in lines:
    if l == []:
        pass
    elif l[0] == 'fold':
        f = l[2].split('=')
        folds.append((0 if f[0] == 'x' else 1, int(f[1])))
    else:
        points.append((int(l[0].split(',')[0]), int(l[0].split(',')[1])))

grid = np.zeros((max(p[0] for p in points)+1, max(p[1] for p in points)+1), dtype=int)

for p in points:
    grid[p[0], p[1]] = 1

def fold(grid, f):
    if f[0] == 0: # fold along x axis
        for j in range(grid.shape[1]):
            for i in range(int((grid.shape[0]-1)/2)):
                # print("adding i idx", f[1]+(f[1]-i), "to", i)
                grid[i,j] += grid[f[1]+(f[1]-i), j]
            for i in range(int((grid.shape[0]-1)/2)+1, grid.shape[0]):
                grid[i,j] = 0
        folded = np.array(grid[:int((grid.shape[0]-1)/2), :], dtype=int)
                
    elif f[0] == 1: # fold along y axis
        for i in range(grid.shape[0]):
            for j in range(int((grid.shape[1]-1)/2)):
                # print("adding j idx", f[1]+(f[1]-j), "to", j)
                grid[i,j] += grid[i, f[1]+(f[1]-j)]
            for j in range(int((grid.shape[1]-1)/2)+1, grid.shape[1]):
                grid[i,j] = 0
        folded = np.array(grid[:, :int((grid.shape[1]-1)/2)], dtype=int)
        
    return folded

f = folds[0]
assert(grid.shape[f[0]] == 2*f[1]+1)
grid = fold(grid, f)
npoints = len(np.where(grid)[0])

print(f"Task 1: After first fold: {npoints} points are visible")     
        
for f in folds[1:]:
     assert(grid.shape[f[0]] == 2*f[1]+1)
     grid = fold(grid, f)

grid[np.where(grid)] = 1
npoints = len(np.where(grid)[0])    
print(f"Task 2: After last fold: {npoints} points are visible, but read the answer yourself:")

np.set_printoptions(linewidth=100)
print(grid.transpose())        

for j in range(grid.shape[1]):
    for i in range(grid.shape[0]):
        print('#' if grid[i,j] else ' ', end="")
    print('\n', end="")
     