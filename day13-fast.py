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

def fold(points, f):
    dims = (max(p[0] for p in points)+1, max(p[1] for p in points)+1)
    pointsToRemove = []
    pointsToAppend = []
    
    if f[0] == 0: # fold along vertical axis (fold x coords)
       for p in points:
           if p[0] > (dims[0]-1)/2:
               pointsToAppend.append((int(f[1]-abs(p[0]-f[1])), p[1]))
               pointsToRemove.append(p)
                
    elif f[0] == 1: # fold along horizontal axis (fold y coords)
         for p in points:
             if p[1] > (dims[1]-1)/2:
                 pointsToAppend.append((p[0], int(f[1]-abs(p[1]-f[1]))))
                 pointsToRemove.append(p)
        
    for p in pointsToRemove:
        points.remove(p)
    points += pointsToAppend
    
    return list(set(points))
        
f = folds[0]
points = fold(points, f)

print(f"Task 1: After first fold: {len(points)} points are visible")     
        
for f in folds[1:]:
      points = fold(points, f)

dims = (max(p[0] for p in points)+1, max(p[1] for p in points)+1)
grid = np.zeros(dims, dtype=bool)
for p in points:
    grid[p] = True
print(f"Task 2: After last fold: {len(points)} points are visible, but read the answer yourself:")

np.set_printoptions(linewidth=100)
# print(grid.transpose())        

for j in range(grid.shape[1]):
    for i in range(grid.shape[0]):
        print('#' if grid[i,j] else ' ', end="")
    print('\n', end="")
     