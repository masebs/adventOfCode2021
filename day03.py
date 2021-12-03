# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

lines = []
with open("input-day03", 'r') as f:
# with open("input-day03-test", 'r') as f:
    lines = f.readlines()
    
vals = []
for l in lines:
    vals.append(l[:-1])


### Task 1
length = len(vals[0])
gamma = 0
epsilon = 0

for i in range(length):
    nzeros = 0
    nones  = 0
    for k, v in enumerate(vals):
        if int(v[i]) == 0:
            nzeros += 1
        else:
            nones  += 1
    
    value = 2**(length-1-i)
    if nzeros > nones: # 0 is most common value at bit position i
        epsilon += value
    else: # 1 is most common value at bit position i
        gamma += value

print(f"Task 1: The decimal values are gamma = {gamma}, epsilon = {epsilon}, product = {gamma*epsilon}")


### Task 2
def filterList(valuelist, useMostCommon):
    vals = valuelist.copy()
    for i in range(len(vals[0])): # for each bit position
        nzeros = 0
        nones  = 0
        for v in vals: # count zeros and ones at bit position i
            if int(v[i]) == 0:
                nzeros += 1
            else:
                nones  += 1
        
        toRemove = []
        if nzeros > nones: # 0 is most common value at bit position i
            for v in vals:
                if (int(v[i]) == 1 and useMostCommon) or (int(v[i]) == 0 and not useMostCommon):
                    toRemove.append(v) # mark for removal
        else: # 1 is most common value at bit position i
            for v in vals:
                if (int(v[i]) == 0 and useMostCommon) or (int(v[i]) == 1 and not useMostCommon):
                    toRemove.append(v) # mark for removal
        
        vals = [v for v in vals if v not in toRemove] # remove marked elements
        
        if len(vals) == 1: # only 1 element left -> that's the value
            # print(f"value found after processing bit {i}")
            return int(vals[0], 2)

oxy = filterList(vals, useMostCommon=True)
co2 = filterList(vals, useMostCommon=False)

print(f"Task 2: The decimal values are oxy = {oxy}, co2 = {co2}, product = {oxy*co2}")

# count lines with grep -cve '^\s*$' -e '^\s*#' day03.py 
#  (actually 4 less due to multiline comment header)
