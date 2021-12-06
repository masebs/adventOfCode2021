# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

with open("input-day06", 'r') as f:
# with open("input-day06-test", 'r') as f:
    lines = f.readlines()
    fish = lines[0][:-1].split(',')
    fish = [(int(i),1) for i in fish]

def run(fish, nrEpochs):
    for i in range(nrEpochs):
        spawncount = sum(f[1] for f in fish if f[0] == 0)
        fish = [(f[0]-1, f[1]) if f[0]-1 >= 0 else (6,f[1]) for f in fish]
        if spawncount > 0:
            fish.append((8, spawncount))
        # print(f"epoch {i}: length {len(fish)}")
    return sum(f[1] for f in fish)
    
print(f"Task 1: Result is {run(fish, 80)}")
print(f"Task 2: Result is {run(fish, 256)}")
