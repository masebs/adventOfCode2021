# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

# with open("input-day22-test") as f:
with open("input-day22") as f:
    lines = [l.split() for l in f.readlines()]

onOff = [1 if l[0] == 'on' else 0 for l in lines]
xyz = [l[1].split(',') for l in lines]
xrange = [[int(i) for i in l[0][2:].split('..')] for l in xyz]
yrange = [[int(i) for i in l[1][2:].split('..')] for l in xyz]
zrange = [[int(i) for i in l[2][2:].split('..')] for l in xyz]

initrange = 50

grid = np.zeros((2*initrange+1, 2*initrange+1, 2*initrange+1), dtype=int)

for k in range(len(xrange)):
    if xrange[k][0] < -initrange or xrange[k][1] > initrange \
        or yrange[k][0] < -initrange or yrange[k][1] > initrange \
        or zrange[k][0] < -initrange or zrange[k][1] > initrange:
        continue
    else:
        if onOff[k] == 1:
            grid[initrange+xrange[k][0]:initrange+xrange[k][1]+1, initrange+yrange[k][0]:initrange+yrange[k][1]+1, initrange+zrange[k][0]:initrange+zrange[k][1]+1] = 1
        else:   
            grid[initrange+xrange[k][0]:initrange+xrange[k][1]+1, initrange+yrange[k][0]:initrange+yrange[k][1]+1, initrange+zrange[k][0]:initrange+zrange[k][1]+1] = 0

ncubes = len(np.where(grid==1)[0])
print(f"Task 1: Number of cubes is {ncubes}")