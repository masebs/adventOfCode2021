# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

from functools import reduce

with open("input-day08", 'r') as f:
# with open("input-day08-test", 'r') as f:
    lines = f.readlines()

lines    = [l.split('|') for l in lines]
patterns = [l[0].split() for l in lines]
output   = [l[1].split() for l in lines]

### Part 1 (could be obtained from within Part 2)
def yieldByLength(length, valuelists):
    for l in valuelists:
        for v in l:
            if len(v) == length:
                yield v
                
# zeros have length 6
count1 = [v for v in yieldByLength(2, output)] # ones have length 2
# twos have length 5
# threes have length 5
count4 = [v for v in yieldByLength(4, output)] # fours have length 4
# fives have length 5
# sixes have length 6
count7 = [v for v in yieldByLength(3, output)] # sevens have length 3
count8 = [v for v in yieldByLength(7, output)] # eights have length 7
# nines have length 6

print(f"Task 1: 1, 4, 7, 8 appear {len(count1)}, {len(count4)}, {len(count7)}, {len(count8)} times, " 
      f"in total: {sum([len(count1), len(count4), len(count7), len(count8)])} times");

### Part 2
# Decodes a 7-digit representation (by segment letters) to the corresponding decimal number
def decode(digit):
    if len(digit) == 7:
        return 8
    elif len(digit) == 6:
        if set(digit) == set(['a', 'b', 'c', 'e', 'f', 'g']):
            return 0
        elif set(digit) == set(['a', 'b', 'd', 'e', 'f', 'g']):
            return 6
        elif set(digit) == set(['a', 'b', 'c', 'd', 'f', 'g']):
            return 9
        else:
            print("WARNING: Unmatched digit!")
    elif len(digit) == 5:
        if set(digit) == set(['a', 'b', 'c', 'e', 'f', 'g']):
            return 0
        elif set(digit) == set(['a', 'b', 'd', 'e', 'f', 'g']):
            return 6
        elif set(digit) == set(['a', 'c', 'd', 'e', 'g']):
            return 2
        elif set(digit) == set(['a', 'c', 'd', 'f', 'g']):
            return 3
        elif set(digit) == set(['a', 'b', 'd', 'f', 'g']):
            return 5
        else:
            print("WARNING: Unmatched digit!")
    elif len(digit) == 4:
        return 4
    elif len(digit) == 3:
        return 7
    elif len(digit) == 2:
        return 1
    else:
        print("WARNING: Unmatched digit!")

# Use the patterns to find the mapping from the actual (standard) segment to the rewired segment:
# segments c,f are the ones from the ones (length 2)
# segment a is the one from 7 which is not c,f -> a identified
# segments b,d are the ones from 4 which are not c,f
# segments e,g are the ones from 8 which are not in c,f,a,b,d
# segment c is the one out of {c,f} which does not appear in all numbers length 6 (0,6,9; c not in 6) -> c,f identified
#      note: works only if there actually is a number 6 contained
# segment d is the one out of {b,d} which does not appear in all numbers length 6 (0,6,9; d not in 0) -> d,b identified
#      note: works only if there actually is a number 0 contained
# segments g is the only one of the unidentified which appears in all numbers length 5 (2,3,5; e not in 3,5) -> g identified
#      note: works only if there actually is a number 3 or 5 contained
# segment e is the last unidentified

mapping = {}
totalsum = 0

for (pat, out) in zip(patterns, output):
    
    # Sort the representations of the pattern by their length 
    len1   = [v for v in pat if len(v)==2]
    len4   = [v for v in pat if len(v)==4]
    len7   = [v for v in pat if len(v)==3]
    len8   = [v for v in pat if len(v)==7]
    len069 = [v for v in pat if len(v)==6]
    len235 = [v for v in pat if len(v)==5]
    
    # Create sets containing the single letters for each list from above
    s1   = set(s for el in len1 for s in el) 
    s4   = set(s for el in len4 for s in el)
    s7   = set(s for el in len7 for s in el)
    s8   = set(s for el in len8 for s in el)
    s069Union     = set(s for el in len069 for s in el) 
    s235Union     = set(s for el in len235 for s in el)
    s069Intersect = reduce(set.intersection, [set(l) for l in len069])
    s235Intersect = reduce(set.intersection, [set(l) for l in len235])
    
    # Apply the rules (set operations) listed above to obtain the mapping
    mapping['cf'] = s1
    mapping['a']  = s7 - mapping['cf']
    mapping['bd'] = s4 - mapping['cf']
    mapping['eg'] = s8 - (mapping['a'] | mapping['cf'] | mapping['bd'])
    mapping['c']  = (s069Union - s069Intersect ) & mapping['cf'] 
    mapping['f']  = mapping['cf'] - mapping['c']
    mapping['d']  = (s069Union - s069Intersect ) & mapping['bd']
    mapping['b']  = mapping['bd'] - mapping['d']
    mapping['g']  = s235Intersect & ({'a', 'b', 'c', 'd', 'e', 'f', 'g'} 
                              - (mapping['a'] | mapping['b'] | mapping['c'] | mapping['d'] | mapping['f'] ) )
    mapping['e']  = {'a', 'b', 'c', 'd', 'e', 'f', 'g'} \
                - (mapping['a'] | mapping['b'] | mapping['c'] | mapping['d'] | mapping['f'] | mapping['g'] )
    
    # We need the mapping in the other direction, so invert it
    invmaplist = [(mapping[k], k) for k in mapping.keys()]
    invmap = {}
    for l in invmaplist:
        if len(l[0]) == 1:
            invmap[list(l[0])[0]] = l[1]
    
    # Use the (inverse) mapping to transfer the representation into standard representation
    number = []
    for o in out:
        # print("o=", o)
        digit = [] 
        for c in o:
            digit.append(invmap[c][0]) # digit is list of segment letters forming the current digit
        # print("digit:", digit)len4
        number.append(decode(digit))   # decode digit into a number

    # print("Number decoded:", number)
    totalsum += number[0]*1000+number[1]*100+number[2]*10+number[3]*1

print(f"Task 2: Sum of all output numbers: {totalsum}")
