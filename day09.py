# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

with open("input-day09", 'r') as f:
# with open("input-day09-test", 'r') as f:
    lines = f.readlines()

rows = []
for l in lines:
    rows.append([int(c) for r in l.split() for c in r])

hmap = np.array(rows)
minpts = []

for i in range(hmap.shape[0]):
    for j in range(hmap.shape[1]):
        val = hmap[i,j]
        cvals = []
        if i-1 >= 0:
            cvals.append(hmap[i-1,j])
        if i+1 < hmap.shape[0]:
            cvals.append(hmap[i+1,j])
        if j-1 >= 0:
            cvals.append(hmap[i,j-1])
        if j+1 < hmap.shape[1]:
            cvals.append(hmap[i,j+1])
        if len([c for c in cvals if c > val]) == len(cvals):
           minpts.append((i,j))

minvals = [hmap[k] for k in minpts]
risk    = [k+1 for k in minvals]
risksum = sum(risk)

print(f"Task 1: Sum of risk levels: {risksum}")

basinsizes = []

for minpt in minpts:
    # print("Investigating minpoint", minpt)
    basinpts = []
    q = [minpt]
    size = 1
    visited = []
    while len(q) > 0:
        c = q.pop()
        if c in visited: # don't investigate a point twice
            continue
        else:
            visited.append(c) # visit each point only once
            # print(" looking at index c=", c)
            idx = []
            if c[0]-1 >= 0:
                idx.append((c[0]-1, c[1]))
            if c[0]+1 < hmap.shape[0]:
                idx.append((c[0]+1, c[1]))
            if c[1]-1 >= 0:
                idx.append((c[0], c[1]-1))
            if c[1]+1 < hmap.shape[1]:
                idx.append((c[0], c[1]+1))
            # print(" idx =", idx)
            for i in idx:
                if hmap[i] > hmap[c] and hmap[i] < 9:  # c is the known basinpt from the q, c the potential new one
                    if i not in basinpts: # avoid adding the same point twice
                        # print(" -> adding to q: point at index i=", i)
                        q.append(i)
                        basinpts.append(i)
                        size += 1
    basinsizes.append(size)

basinsizes.sort(reverse=True)
# print(basinsizes)
result = basinsizes[0] * basinsizes[1] * basinsizes[2]

print(f"Task 2: Product of three largest basin sizes is {result}")

