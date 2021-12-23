# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

test = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
  
inputdata = """#############
#...........#
###B#B#C#D###
  #D#A#A#C#
  #########"""

def printGrid(grid):
    for l in grid:
        for v in l:
            if v == 0:
                c = '#'
            elif v == 1:
                c = 'A'
            elif v == 2:
                c = 'B'
            elif v == 3:
                c = 'C'
            elif v == 4:
                c = 'D'
            elif v == 9:
                c = '.'
            print(c, end="")
        print('\n', end="")
        
inpt = test

lines = inpt.split('\n')

grid = np.zeros((len(lines), len(lines[0])), dtype=int)

for i, l in enumerate(lines):
    for j, c in enumerate(l):
        if c == '#':
            val = 0
        elif c == '.':
            val = 9
        elif c == 'A':
            val = 1
        elif c == 'B':
            val = 2
        elif c == 'C':
            val = 3
        elif c == 'D':
            val = 4
            
        grid[i,j] = val
        

def searchMotion(grid, player=0, previousdir=(0,0), previouscost=0):
    
    possibleMotions = []
    forbiddenStops = [(1,3), (1,5), (1,7), (1,9)]

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i,j] != 0 and grid[i,j] != 9:
                dirs = [(m, n) for m in range(-1,2) for n in range(-1,2) if i+m >= 0 and i+m < grid.shape[0] and j+n >= 0 and j+n < grid.shape[1] and m != n and (m == 0 or n == 0)]
                
                for d in dirs:
                    if grid[i+d[0], j+d[1]] == 9:
                        cost = 10**(grid[i,j]-1)
                        if (i+d[0], j+d[1]) not in forbiddenStops:
                            possibleMotions.append([i, j, grid[i,j], (previousdir[0]+d[0], previousdir[1]+d[1]), previouscost+cost])
                        grid[i+d[0], j+d[1]] = grid[i, j]
                        possibleMotions += searchMotion(grid.copy(), player, (previousdir[0]+d[0], previousdir[1]+d[1]), previouscost+cost)
                        
    return possibleMotions
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    