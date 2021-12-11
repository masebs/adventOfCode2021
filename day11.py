# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

with open("input-day11", 'r') as f:
# with open("input-day11-test", 'r') as f:
    lines = [[int(i) for i in l.split()[0]] for l in f.readlines()]

grid = np.array(lines, dtype=int)

# nEpochs = 100
flashcount  = 0
synchronous = False

# for k in range(nEpochs):
k = 0
while not synchronous:  # run through time steps until flashed are synchronized
    k += 1
    grid += 1
    xcoords, ycoords = np.where(grid == 10)
    flashing = [(xcoords[n], ycoords[n]) for n in range(xcoords.shape[0]) ] # currently flashing
    flashed  = flashing.copy() # flashed during this time step
    
    while flashing: # iterate as long as there are any flashes
        for f in flashing:
            grid[f] = 0      # flashed element at index f: set to zero and count
            flashcount += 1
            neighbrs = [(f[0]+i, f[1]+j) for i in range(-1,2) for j in range(-1,2) 
                         if f[0]+i >= 0 and f[1]+j >= 0 and f[0]+i < grid.shape[0] and f[1]+j < grid.shape[1] ]
            for n in neighbrs: # increment all neighbours if they didn't flash already
                if n not in flashed:
                    grid[n] += 1
        xcoords, ycoords = np.where(grid >= 10) # need to consider > 10 as well, as they might have received several flashes
        critVal  = [(xcoords[n], ycoords[n]) for n in range(xcoords.shape[0]) ]
        flashing = [f for f in critVal if f not in flashed] # sort out those who have already flashed before in this step
        flashed += flashing # save all newly flashed indices for later
        if len(flashed) == grid.shape[0]*grid.shape[1]: # if all have flashed within this step: done!
            synchronous = True
    
    if k == 100:
        print(f"Task 1: Flash count after {k} steps is: {flashcount}")
    
print(f"Task 2: Flashes synchronized after {k} steps")        


        
        
        