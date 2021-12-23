# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np
from itertools import combinations

with open("input-day22-test1") as f:
# with open("input-day22") as f:
    #lines = [l.split() for l in f.readlines()]
    lines = [l.split() for l in f.readlines()[:-2]]

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

cubes = [] # contains ranges of cubes which are on, and some inverts within them

def overlapCoord(list1, list2):
    fromval = max((list1[0], list2[0]))
    toval   = min((list1[-1], list2[-1]))
    if fromval < toval:
        return [fromval, toval]
    else:
        return []

def overlapCube(cube1, cube2):
    if cube1 == [] or cube2 == []:
        return []
    else:
        overlaps = []
        for k in range(3):
            o = overlapCoord(cube1[k], cube2[k])
            if not o: # if (at least) one coord does not overlap, the cube does not overlap
                return [] 
            overlaps.append(o)
        return overlaps
        
def cubeVolume(cube):
    if cube == []:
        return 0
    else:
        xsize = cube[0][-1] - cube[0][0] + 1
        ysize = cube[1][-1] - cube[1][0] + 1
        zsize = cube[2][-1] - cube[2][0] + 1
        cubevol = xsize * ysize * zsize
        return cubevol

def findIntersects(cubes):
    intersects = {}
    for k in range(len(cubes)):
        intersects[k] = []

    for i, cube1 in enumerate(cubes):
        for j, cube2 in enumerate(cubes):
            if i == j:
                continue
            if overlapCube(cube1, cube2):
                intersects[i].append(j)
    return intersects

def getVolumeWithOverlap(cubenr, allcubes, overlapping):
    cube = allcubes[cubenr]
    volume = cubeVolume(cube)
    print(" adding single volume:", cubeVolume(cube))
    sign = 1
    for l in range(len(overlapping)):
        sign *= -1
        combs = list(combinations([cubenr]+overlapping, l+2))
        # print(l, sign, combs)
        for comb in combs:
            cInt = allcubes[comb[0]]
            if cInt[3] == 0: # cInt is an "off" cube
                continue
            for c in comb[1:]:
                othercube = allcubes[c]
                if othercube[3] == 0:
                    cInt = []
                    break
                else:
                    cInt = overlapCube(cInt, othercube)
                    if cInt == []:
                        break
            # print("   adding to totalvolume", comb, sign*cubeVolume(cInt))
            volume += sign * cubeVolume(cInt)
    print("Returning volume", volume)
    return volume


for k in range(len(xrange)):
    cubes.append([xrange[k], yrange[k], zrange[k], onOff[k]]) # last list: invert coords

intersects = findIntersects(cubes)

totalvolume = 0
correction  = 0
maxoverlaps = 0
for k in intersects.keys():
    if len(intersects[k]) > maxoverlaps:
        maxoverlaps = len(intersects[k])

for i, cube in enumerate(cubes):
    overlapping = intersects[i]
    if cube[3]: # "on" cube
        totalvolume += getVolumeWithOverlap(i, cubes, overlapping)
    # else: # "off" cube
    #     overlapping = intersects[i]
    #     corrvol = 0
    #     sign = 1
    #     for l in range(2, maxoverlaps+1): # combination lengths
    #         sign *= -1
    #         combs = list(combinations(overlapping, l))
    #         # print(l, sign, combs)
    #         for comb in combs:
    #             cInt = cubes[comb[0]]
    #             if cInt[3] == 0: # cInt is an "off" cube
    #                 continue
    #             assert(len(comb) == l)
    #             for c in comb[1:]: # iterate through combinations
    #                 othercube = cubes[c]
    #                 if othercube[3] == 0:
    #                     cInt = []
    #                     break
    #                 else:
    #                     cInt = overlapCube(cInt, othercube)
    #                     if cInt == []:
    #                         break
    #             print("   adding to corrvol", comb, sign*cubeVolume(cInt))
    #             corrvol += sign * cubeVolume(cInt)
    #     assert(abs(corrvol) < cubeVolume(cube))
    #     print("corrvol:", corrvol)
    #     totalvolume += corrvol


print(f"Task 2: Total volume is {totalvolume}")


allcubes = [ [[ 0, 3], [ 0, 3], [ 0, 3], 1], 
             [[-1, 1], [-1, 1], [-1, 1], 1], 
             [[ 1, 2], [ 1, 2], [ 1, 2], 1],
             [[-5, 5], [-5, 5], [-5, 5], 1]
           ]
overlapping = [2]
getVolumeWithOverlap(0, allcubes, overlapping)


