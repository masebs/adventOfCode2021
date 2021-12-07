# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

with open("input-day07", 'r') as f:
# with open("input-day07-test", 'r') as f:
    lines = f.readlines()
    hpos = lines[0][:-1].split(',')
    hpos = [int(i) for i in hpos]

def alignAt(hpos, alignpos):
    return sum(abs(h-alignpos) for h in hpos)

fuel = [alignAt(hpos, p) for p in range(max(hpos))]
minfuel = min(fuel)
minidx = fuel.index(minfuel)
opthpos = hpos[minidx]

print(f"Task 1: Result is {minfuel}")

# Very inefficient but works for this case; already computed data should be reused
# def alignAt2(hpos, alignpos):
#     return sum(sum(range(abs(h-alignpos)+1)) for h in hpos)
# Use Gauss' summation formula to calculate 1+2+...+abs(h-alignpos)
# Faster than calculating sum by a factor of at least 20
def alignAt2(hpos, alignpos):
    return int(sum(0.5*abs(h-alignpos)*(abs(h-alignpos)+1) for h in hpos)) 

fuel = [alignAt2(hpos, p) for p in range(max(hpos))]
minfuel = min(fuel)
minidx = fuel.index(minfuel)
opthpos = hpos[minidx]

print(f"Task 2: Result is {minfuel}")
