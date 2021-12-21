# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

from itertools import permutations

# with open("input-day19", 'r') as f:
with open("input-day19-test", 'r') as f:
    lines = f.readlines()

scanners = []
plist = []

for l in lines:
    if l.startswith('--- scanner'):
        if plist:
            scanners.append([tuple(p) for p in plist])
        plist = []
    elif len(l) > 1:
        plist.append([int(i) for i in l.split()[0].split(',')])   
scanners.append([tuple(p) for p in plist])

def getRotations(pts): # get all 24 allowed rotations
    transforms = [m for n in 
                 [list(permutations(comb)) for comb in 
                 [(i,j,k) for i in [-1,1] for j in [-2,2] for k in [-3,3]]] 
                 for m in n] # 49, all systems including left-hand systems; right-handed would probably suffice!
    rots = [doTransform(pts, trafo) for trafo in transforms]
    return rots, transforms

def doTransform(pts, trafo):
    return [tuple(p[abs(k)-1] * k//abs(k) for k in [t for t in trafo]) for p in pts]

def doOffset(pts, offset):
    return [tuple([p[0]+offset[0], p[1]+offset[1], p[2]+offset[2]]) for p in pts] 

transformedTo = {}
offsets = {}
transforms = {}
for s in range(len(scanners)):
    transformedTo[s] = []
    offsets[s] = []
    transforms[s] = []

for i in range(len(scanners)):
    for j in range(len(scanners)):
        if i == j: # for j in transformedTo.keys():
            continue
        s1 = scanners[i]
        s2Rots, trafo = getRotations(scanners[j])
        done = False
        
        for s2nr, s2 in enumerate(s2Rots):
            for s1p in s1:
                for s2p in s2:
                    offset = [s1p[k] - s2p[k] for k in range(3)]
                    s2moved = doOffset(s2, offset)
                    common = [p for p in s1 if p in s2moved]
                
                    if len(common) >= 12:
                        offsets[j].append(offset)
                        transforms[j].append(trafo[s2nr])
                        transformedTo[j].append(i)
                        print("i, j, common points", i, j, len(common))
                        print("transform nr", s2nr, trafo[s2nr])
                        print("offset", offset)
                        # print("common:", common)
                        print()
                        done = True
                        
                    if done:
                        break
                if done:
                    break
            if done:
                break
        

def findPathTo0(transformedTo, key, visited=None):
    if visited == None:
        visited = []
    if key in visited:
        return ([], [])
    visited.append(key)
    t = transformedTo[key]
    if 0 in t:
        return ([t.index(0)], [0])
    else:
        # print(t)
        for tt in t:
            # print("  ", tt)
            res, keys = findPathTo0(transformedTo, tt, visited)
            if len(res) > 0:
                res.append(t.index(tt))
                keys.append(tt)
                return (res, keys)
        return ([], [])
        

stransformed = [scanners[i] for i in range(len(scanners))]

keysToTransform = [k for k in transformedTo.keys() if k != 0]
# print(transformedTo); print()

for key in keysToTransform:
    path, pathkeys = findPathTo0(transformedTo, key)
    print(f"Transforming from {key} to 0 along path {pathkeys[::-1]}")
    
    pkey = key
    tf = stransformed[pkey]
    while path:
        tidx = path.pop()
        print(f"  using pkey: {pkey}, tidx: {tidx}")
        tf = doTransform(tf, transforms[pkey][tidx])
        tf = doOffset(tf, offsets[pkey][tidx])
        pkey = pathkeys.pop()
        
    stransformed[key] = tf
            
finalpoints = list(set([p for st in stransformed for p in st]))        

print(f"\nTask 1: There are {len(finalpoints)} distinct points")

def manhattanDist(p1, p2):
    return sum(abs(p1[k]-p2[k]) for k in range(3))

offsetsToZero = {}
for okey in offsets.keys():
    path, pathkeys = findPathTo0(transformedTo, okey)
    pkey = okey
    to = [[0,0,0]]
    while path:
        tidx = path.pop()
        # print(tidx, pkey, to, offsets[pkey][tidx])
        to = doTransform(to, transforms[pkey][tidx])
        to = doOffset(to, offsets[pkey][tidx])
        pkey = pathkeys.pop()
    offsetsToZero[okey] = to
# print(offsetsToZero)

maxdist = 0
for o1 in offsetsToZero.values():
    for o2 in offsetsToZero.values():
        dist = manhattanDist(o1[0], o2[0])
        if dist > maxdist:
            maxdist = dist
            
print(f"Task 2: Max scanner dist is {maxdist}")
        