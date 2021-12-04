# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

lines = []
with open("input-day04", 'r') as f:
# with open("input-day04-test", 'r') as f:
    lines = f.readlines()
lines.append('\n')

# Read numbers drawn
line1 = lines[0][:-1].split(',')
nrs   = np.array(line1, dtype=int)

# Read boards
rows = []
fields = []

for l in lines[2:]:
    if l == '\n':
        fields.append(np.array(rows, dtype=int))
        rows = []
    else:
        rows.append(l[:-1].split())

# Play all boards
winboards = []
winboardNrs = []
winNr  = []
for n in nrs:
    print(n)
    for i, f in enumerate(fields):
        if not i in winboardNrs:
            hitlines, hitcols = np.where(f == n)
            f[hitlines, hitcols] = -1
            if np.sum(f[hitlines,:]) == -f.shape[0] or np.sum(f[:,hitcols]) == -f.shape[1]:
               winboards.append(f.copy())
               winboardNrs.append(i)
               winNr.append(n)

# Evaluate first winning board
unmarkedRows, unmarkedCols = np.where(winboards[0] != -1)   
unmarkedSum = np.sum(winboards[0][unmarkedRows, unmarkedCols])
res = winNr[0]*unmarkedSum

print(f"Task 1: Result is {res}")

# Evaluate last winning board
unmarkedRows, unmarkedCols = np.where(winboards[-1] != -1)   
unmarkedSum = np.sum(winboards[-1][unmarkedRows, unmarkedCols])
res = winNr[-1]*unmarkedSum

print(f"Task 2: Result is {res}")

# count lines with grep -cve '^\s*$' -e '^\s*#' day03.py 
#  (actually 4 less due to multiline comment header)
