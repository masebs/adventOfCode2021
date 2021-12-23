# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np
from itertools import combinations

with open("input-day22-test0") as f:
# with open("input-day22") as f:
    lines = [l.split() for l in f.readlines()]
    # lines = [l.split() for l in f.readlines()[:-2]]

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
    print(f"After step {k}: {len(np.where(grid==1)[0])}")
    
ncubes = len(np.where(grid==1)[0])
print(f"\nTask 1: Number of cubes is {ncubes}\n")

def overlapCoord(list1, list2):
    fromval = max((list1[0], list2[0]))
    toval   = min((list1[-1], list2[-1]))
    if fromval <= toval:
        return [fromval, toval]
    else:
        return []

def intersectCubes(cube1, cube2):
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
        assert(cubevol >= 0)
        return cubevol

def findIntersects(cubes):
    intersects = {}
    for k in range(len(cubes)):
        intersects[k] = []

    for i, cube1 in enumerate(cubes):
        for j, cube2 in enumerate(cubes):
            if i == j:
                continue
            if intersectCubes(cube1, cube2):
                intersects[i].append(j)
    return intersects

def findIntersectsSingleCube(cubes, cube1):
    intersects = []
    for j, cube2 in enumerate(cubes):
        if cube2 != cube1 and intersectCubes(cube1, cube2):
            intersects.append(j)
    return intersects

def getVolumeWithOverlap(cubenr, cubes, overlapping, diffvol=False):
    cube = cubes[cubenr]
    if diffvol:
        volume = 0
    else:
        volume = cubeVolume(cube)
    sign = 1
    for l in range(len(overlapping)):
        sign *= -1
        combs = [c for c in combinations([cubenr]+overlapping, l+2) if cubenr in c]
        for comb in combs:
            cInt = cubes[comb[0]]
            for c in comb[1:]:
                othercube = cubes[c]
                cInt = intersectCubes(cInt, othercube)
                if cInt == []:
                    break
            volume += sign * cubeVolume(cInt)
    if not diffvol:
        assert(volume >= 0)
    return volume

def splitInterval(tosplit, splitby):
    minimum = min(tosplit[0], splitby[0])
    maximum = max(tosplit[1], splitby[1])
    
    if minimum == tosplit[0]:
        lowval = [[minimum, splitby[0]-1]]
    else:
        lowval = [[splitby[0], tosplit[0]]]
    if maximum == tosplit[1]:
        highval = [[splitby[1]+1, maximum]]
    else:
        highval = []
    if tosplit[1] < splitby[0] or splitby[1] < tosplit[0]: # don't intersect
        return []
    return lowval + [splitby] + highval

def splitCube(cube, splitby):
    xints = splitInterval(cube[0], splitby[0])
    yints = splitInterval(cube[1], splitby[1])
    zints = splitInterval(cube[2], splitby[2])
    
    return [[x, y, z] for x in xints for y in yints for z in zints]
    
def subtractCube(offcube, cubes, overlapping):
    overlappingCubes = [cubes[i] for i in overlapping]
    toRemove = []
    toAppend = []
    
    while overlappingCubes:
        oncube = overlappingCubes[0]
        overlappingCubes.remove(oncube)
        splitcubes = splitCube(oncube, offcube)
        splitcubes.remove(offcube)
        
        for c in splitcubes:
            toAppend.append(c)
        
    for r in toRemove:
        cubes.remove(r)
    for a in toAppend:
        discard = False
        # for c in cubes:
        #     if splitCube(a, c)[0] == a:
        #         print("discarding")
        #         discard = True
        if not discard:
            cubes.append(a)

def isContained(cubeInner, cubeOuter):
    return all([i[0] >= o[0] for i in cubeInner for o in cubeOuter] + [i[1] <= o[1] for i in cubeInner for o in cubeOuter])
      
cubes = [] # contains ranges of cubes which are on, and some inverts within them
totalvolume = 0

for k in range(len(xrange)):
    cube = [xrange[k], yrange[k], zrange[k]]
    
    if onOff[k]: # "on" cube
        overlapping = findIntersectsSingleCube(cubes, cube)
        toRemove = []
        toAppend = []
        for o in overlapping:
            toRemove.append(cubes[o])
            toAppend += splitCube(cubes[o], cube)
            toAppend.remove(cube)
            # for a in toAppend:
            #     if isContained(a, cube):
            #         toRemove.append(a)
        
        for a in toAppend:
            cubes.append(a)
        for r in toRemove:
            cubes.remove(r)
        cubes.append(cube)
        # toRemove = []
        # for c in cubes:
        #     if c != cube and isContained(c, cube):
        #         toRemove.append(c)
        # print(toRemove)
        # for r in toRemove:
        #     cubes.remove(r)
        volume = 0
        for c in cubes:
            # print(cubeVolume(c))
            volume += cubeVolume(c)
        totalvolume = volume
    else: # "off" cube
        # raise Exception()
        cubes.append(cube)
        overlapping = findIntersectsSingleCube(cubes, cube)
        totalvolume += getVolumeWithOverlap(cubes.index(cube), cubes, overlapping, diffvol=True)
        cubes.remove(cube)
        subtractCube(cube, cubes, overlapping)
        
    print(f"After step {k}: {totalvolume}")


print(f"\nTask 2: Total volume is {totalvolume}\n")


# cubes = [ [[ 0, 3], [ 0, 3], [ 0, 3], 1], 
#           [[-1, 1], [-1, 1], [-1, 1], 1], 
#           [[ 1, 2], [ 1, 2], [ 1, 2], 1],
#           [[-5, 5], [-5, 5], [-5, 5], 0]
#         ]
# overlapping = [0,2,3]
# getVolumeWithOverlap(1, cubes, overlapping, diffvol=True)


