# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

lines = []
with open("input-day06", 'r') as f:
# with open("input-day06-test", 'r') as f:
    lines = f.readlines()
    fish = lines[0][:-1].split(',')
    fish = [(int(i),1) for i in fish]

def run(fish, nrEpochs):
    for i in range(nrEpochs):
        spawncount = sum([f[1] for f in fish if f[0] == 0])
        fish = [(i[0]-1, i[1]) if i[0]-1 >= 0 else (6,i[1]) for i in fish]
        if (spawncount > 0):
            fish.append((8, spawncount))
        # print(f"epoch {i}: length {len(fish)}")
    return sum(f[1] for f in fish)
    
print(f"Task 1: Result is {run(fish, 80)}")
print(f"Task 1: Result is {run(fish, 256)}")
