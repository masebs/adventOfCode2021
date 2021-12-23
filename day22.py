# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

# with open("input-day22-test2") as f:
with open("input-day22") as f:
    #lines = [l.split() for l in f.readlines()]
    lines = [l.split() for l in f.readlines()]

onOff = [1 if l[0] == 'on' else 0 for l in lines]
xyz = [l[1].split(',') for l in lines]
xrange = [[int(i) for i in l[0][2:].split('..')] for l in xyz]
yrange = [[int(i) for i in l[1][2:].split('..')] for l in xyz]
zrange = [[int(i) for i in l[2][2:].split('..')] for l in xyz]

### Part 1: Completely dumb simulution with a full numpy array. Obviously won't work for part 2

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

### Part 2: Strategy is: For a new cube, clear its volume range before inserting by deleting any cubes which are
#           compeletely contained in the new cube, and split those are intersecting but not contained into sub-cubes
#           which align with the borders of the new cube. Delete all subcubes which are contained in the new cube.
#           Then, for "on" cubes, insert the new cube into the free space. For "off" cubes, do nothing more, their
#           space has been cleared. There are no intersections or containments in the cube array at any time, 
#           so the volume can be calculated at any time by adding the volumes of all cubes.
#           Using the principle of inclusion and exclusion would also work if the cubes are propely united at the 
#           insertion. Adding them as they are causes inclusion and exclusion to run for an eternity because each 
#           cube is intersecting with many other cubes, and n! intersections need to be calculated if n is the number 
#           of intersecting cubes
    
def isContiguous(int1, int2):
    s = sorted([int1, int2], key = lambda i: i[0])
    if s[0][1] < s[1][0]:
        return False
    else:
        return True

def splitInterval(int1, int2):
    if not isContiguous(int1, int2):
        return [ int1, int2 ]
    elif int1 == int2:
        return [int1]
    else:
        v0 = min(int1[0], int2[0])
        v1 = int1[0] if v0 == int2[0] else int2[0]
        v3 = max(int1[1], int2[1])
        v2 = int1[1] if v3 == int2[1] else int2[1]
        return [ [v0, v1-1], [v1, v2], [v2+1, v3] ] # split values apper in the middle segment, not the outer ones
        
def splitCube(tosplit, splitby): # splits tosplit at the boundaries of splitby; volume afterwards is same as for tosplit
    xints = splitInterval(tosplit[0], splitby[0])
    yints = splitInterval(tosplit[1], splitby[1])
    zints = splitInterval(tosplit[2], splitby[2])
   
    splitcubes = [[x, y, z] for x in xints for y in yints for z in zints]
    splitcubes = [s for s in splitcubes if isCubeContained(s, tosplit)]
    return splitcubes

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
    
def findIntersects(cubes, cube1):
    intersects = []
    for j, cube2 in enumerate(cubes):
        if cube2 != cube1 and intersectCubes(cube1, cube2):
            intersects.append(j)
    return intersects

def isCubeContained(cubeInner, cubeOuter):
    if intersectCubes(cubeInner, cubeOuter) == cubeInner:
        return True
    else:
        return False

cubes = [] # contains only non-intersecting, non-contained cubes

for k in range(len(xrange)):
    cube = [xrange[k], yrange[k], zrange[k]]
    overlapping = findIntersects(cubes, cube)
    toRemove = []
    toAppend = []

    changes = 1
    while changes > 0:
        toRemove = []
        toAppend = []
        for c in cubes:
            if isCubeContained(c,cube) and c != cube and c not in toRemove:
                # print(f"{c} is contained in {cube}, remove it!")
                toRemove.append(c)
            intersect = intersectCubes(c, cube) 
            if intersect and c != cube and c not in toRemove:
                # print(f"{c} intersects with {cube}, splitcube({c}, {cube}) !")
                toRemove.append(c)
                toAppend += splitCube(c, cube)
        for r in toRemove:
            cubes.remove(r)
        for a in toAppend:
            cubes.append(a)
        
        changes = len(toRemove) + len(toAppend)
        
    if onOff[k] == 1 and cube not in cubes:
        cubes.append(cube)
        
    for c in cubes:
        if c != cube:
            assert(not intersectCubes(c, cube))
            assert(not isCubeContained(c, cube))
    
    totalvolume = 0
    for c in cubes: # obviously faster when commented out
        totalvolume += cubeVolume(c)
    print(f"After step {k}: {totalvolume}")
    
totalvolume = 0
for c in cubes:
    totalvolume += cubeVolume(c)   
    
print(f"\nTask 2: Number of cubes is {totalvolume}\n") 
