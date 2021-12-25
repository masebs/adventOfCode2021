# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

with open("input-day25") as f:
    lines = f.readlines()
lines = [l.split()[0] for l in lines]

grid = np.zeros((len(lines), len(lines[0])), dtype=int)                  

for row, l in enumerate(lines):
    for col, c in enumerate(l):
        grid[row, col] = 1 if c == '>' else (2 if c == 'v' else 0)
            
print(grid)
moves = 1
movecount = 0

while moves:
    moves = 0
    movecount += 1
    
    rightidcs = np.where(grid == 1)
    downidcs  = np.where(grid == 2)
    
    toMove = []
    for k in range(rightidcs[0].shape[0]):
        row = rightidcs[0][k]
        col = rightidcs[1][k]
        if col+1 < grid.shape[1]:
            nextidx = col+1
        else:
            nextidx = 0
        if grid[row, nextidx] == 0:
            moves += 1
            toMove.append([(row, col), (row, nextidx)])
    for idcs in toMove:
        grid[idcs[1]] = grid[idcs[0]]
        grid[idcs[0]] = 0
    
    toMove = []        
    for k in range(downidcs[0].shape[0]):
        row = downidcs[0][k]
        col = downidcs[1][k]
        if row+1 < grid.shape[0]:
            nextidx = row+1
        else:
            nextidx = 0
        if grid[nextidx, col] == 0:
            moves += 1
            toMove.append([(row, col), (nextidx, col)])
    for idcs in toMove:
        grid[idcs[1]] = grid[idcs[0]]
        grid[idcs[0]] = 0
        
print(grid)

print(f"\nTask 1: Number of moves: {movecount}")