# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc s schneider @ mailbox org
"""

lines = []
with open("input-day02", 'r') as f:
# with open("input-day02-test", 'r') as f:
    lines = f.readlines()
    
vals = []
for l in lines:
    vals.append(l[:-1].split(' '))
    
hpos  = 0
depth = 0

for v in vals:
    if v[0] == 'forward':
        hpos += int(v[1])
    elif v[0] =='down':
        depth += int(v[1])
    elif v[0] == 'up':
        depth -= int(v[1])

print(f"Task 1: Horizontal position: {hpos}, depth: {depth}, product {hpos*depth}")

hpos  = 0
depth = 0
aim   = 0

for v in vals:
    if v[0] == 'forward':
        hpos  += int(v[1])
        depth += aim*int(v[1])
    elif v[0] =='down':
        aim += int(v[1])
    elif v[0] == 'up':
        aim -= int(v[1])

print(f"Task 2: Horizontal position: {hpos}, depth: {depth}, product {hpos*depth}")