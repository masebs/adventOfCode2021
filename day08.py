# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

# with open("input-day08", 'r') as f:
with open("input-day08-test", 'r') as f:
    lines = f.readlines()

lines    = [l[:-1].split('|') for l in lines]
patterns = [l[0].split() for l in lines]
output   = [l[1].split() for l in lines]

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

# segments c,f are the ones included in all four easy values 1,4,7,8 
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

pat = patterns[0]
len1   = [v for v in pat if len(v)==2]
len4   = [v for v in pat if len(v)==4]
len7   = [v for v in pat if len(v)==3]
len8   = [v for v in pat if len(v)==7]
len069 = [v for v in pat if len(v)==6]
len235 = [v for v in pat if len(v)==5]

s1   = set(s for el in len1 for s in el) 
s4   = set(s for el in len4 for s in el)
s7   = set(s for el in len7 for s in el)
s8   = set(s for el in len8 for s in el)
s069 = [set(l) for l in len069] 
s235 = [set(l) for l in len235] 

identifiedSet = set()

mapping['cf'] = list(s1) 
mapping['a']  = list(s7 - (s1 & s4 & s7 & s8))[0]
identifiedSet |= set(mapping['a'])
mapping['bd'] = list(s4 - set(mapping['cf']))
mapping['eg'] = list(s8 - (set(mapping['a']) | set(mapping['cf']) | set(mapping['bd'])))
mapping['c']  = list( ((s069[0] | s069[1] | s069[2]) - (s069[0] & s069[1] & s069[2]) ) & set(mapping['cf']) )
mapping['f']  = list(set(mapping['cf']) - set(mapping['c']))
mapping['d']  = list( ((s069[0] | s069[1] | s069[2]) - (s069[0] & s069[1] & s069[2]) ) & set(mapping['bd']) )
mapping['b']  = list(set(mapping['bd']) - set(mapping['d']))
mapping['g']  = list( ( (s235[0] & s235[1] & s235[2]) 
                       & ({'a', 'b', 'c', 'd', 'e', 'f', 'g'} 
                          - (set(mapping['a']) | set(mapping['b']) | set(mapping['c']) | set(mapping['d']) | set(mapping['f']) ) )
                       ))
mapping['e']  = list({'a', 'b', 'c', 'd', 'e', 'f', 'g'} 
                     - (set(mapping['a']) | set(mapping['b']) | set(mapping['c']) | set(mapping['d']) | set(mapping['f']) | set(mapping['g']) ))

def decodeOutput(output, mapping):
    for o in output:
        for c in o:
            c = ...
