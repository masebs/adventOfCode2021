# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

lines = []
with open("input-day01", 'r') as f:
# with open("input-day01-test", 'r') as f:
    lines = f.readlines()
    
vals = []

for l in lines:
    vals.append(int(l[:-1]))
    
nrInc = 0
prev = 0

slidingAvg = 0
prevSlidingAvg = 0
nrAvgInc = 0

for i,l in enumerate(vals):
    if i>0:
        #print(l-prev)
        if l-prev > 0:
            nrInc += 1
    if i>2:
        slidingAvg = l + vals[i-1] + vals[i-2]
        if slidingAvg > prevSlidingAvg:
            nrAvgInc += 1
            
    prev = l
    prevSlidingAvg = slidingAvg
    

print(f"Task 1: Value increased {nrInc} times")
print(f"Task 2: Value increased {nrAvgInc} times")  