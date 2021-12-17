# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

target = [np.array(range(277, 318+1)), np.array(range(-92, -53+1))] # the task
# target = [np.array(range(20, 30+1)), np.array(range(-10, -5+1))] # the example

def sim(curpos, speed, target):
    path = []
    while not (curpos[0] in target[0] and curpos[1] in target[1]):
        curpos = curpos + speed
        
        if speed[0] > 0:
            speed[0] -= 1
        elif speed[0] < 0:
            speed[0] += 1
        speed[1] -= 1
        
        if curpos[1] < np.min(target[1]): # missed target
            return []
        else:
            path.append(curpos)
        
    return path

maxheight = 0
maxheightspeed = np.array([0, 0])
pos = np.array([0, 0])
speedrange = [range(0, 320), range(-100, 100)]
hitcount = 0
# hits = []

for xv in speedrange[0]:
    for yv in speedrange[1]:
        speed = np.array([xv, yv])        
        path = sim(pos, speed.copy(), target)
        if path:
            hitcount += 1
            # hits.append((speed[0], speed[1]))
            maxy = max(p[1] for p in path)
            if maxy > maxheight:
                maxheight = maxy
                maxheightspeed = speed.copy()
                
print(f"Task 1: Maximum height {maxheight}")
print(f"Task 2: {hitcount} hits")

# maxx = max(h[0] for h in hits)
# minx = min(h[0] for h in hits)
# maxy = max(h[1] for h in hits)
# miny = min(h[1] for h in hits)
# print(f"x in {minx}...{maxx}, y in {miny}...{maxy}")

