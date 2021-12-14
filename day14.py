# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

with open("input-day14", 'r') as f:
# with open("input-day14-test", 'r') as f:
    lines = [l.split() for l in f.readlines()]
poly = lines[0][0]
rules = dict([(l[0], l[2]) for l in lines[2:]])

### Naive approach for task 1: Write the full length (feasible for up to 20 steps)
# nSteps = 10
#
# for n in range(nSteps):
#     pairs  = [poly[i] + poly[i+1] for i in range(len(poly)-1)]
#     insert = [rules[p] for p in pairs] 
#     merge  = ''
#     assert(len(poly) == len(insert) + 1)
#     for k in range(len(insert)):
#         merge += poly[k] + insert[k]
#     merge += poly[len(poly)-1] # last element
#     poly = merge
#     print(f"length after step {n+1}: {len(poly)}")

# elems = list(set(poly))
# elemnrs = []       
# for e in elems:
#     elemnrs.append(poly.count(e))
# res = max(elemnrs) - min(elemnrs)

# print(f"\nTask 1: The result is {res}\n")

### Efficient approach for task 2: Only save number of occurences of elements and neighborhoods 
nSteps = 40

elems = '' # list of (unique) elements
for r in rules.keys():
    elems += r
elems = list(set(elems))

occ = {}   # numbers of occurence for each element
for o in elems:
    occ[o] = poly.count(o)

perms = [] # all available permutations of the elements (these are all possible neighborhoods)
for i,e in enumerate(elems):
    for f in elems[i:]:
        perms += [e+f]
        if e != f:
            perms += [f+e]
            
nhood = {} # numbers of occurence for each neighborhood (i.e. for each possible pair)
for p in perms:
    nhood[p] = poly.count(p)

for n in range(nSteps):
    newocc   = occ.copy()    # copy because changes should not take effect before all nhoods are processed
    newnhood = nhood.copy()
    for p in nhood.keys():
        pair1 = p[0] + rules[p]       # new pair 1
        pair2 = rules[p] + p[1]       # new pair 2
        newnhood[pair1]  += nhood[p]  # increase nhood for first new pair 
        newnhood[pair2]  += nhood[p]  # increase nhood for second new pair
        newnhood[p]      -= nhood[p]  # decrease nhood for old pair
        newocc[rules[p]] += nhood[p]  # increase occurences for inserted element
    nhood = newnhood  # let changes take effect for the next step
    occ   = newocc
    
    length = sum(occ[k] for k in occ.keys()) # just for output
    print(f"length after step {n+1}: {length}")
    
    if n == 9: # evaluate part 1 result
        elemnrs = [occ[e] for e in elems]
        res = max(elemnrs) - min(elemnrs)
        print(f"\nTask 1: The result is {res}\n")
    
elemnrs = [occ[e] for e in elems]
res = max(elemnrs) - min(elemnrs)

print(f"\nTask 2: The result is {res}")
