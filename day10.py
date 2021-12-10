# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

with open("input-day10", 'r') as f:
# with open("input-day10-test", 'r') as f:
    lines = [l.split()[0] for l in f.readlines()]

# Part 1
stack  = []
pairs  = {'(': ')', '[': ']', '{': '}', '<': '>'}
points = {')': 3, ']': 57, '}': 1197, '>': 25137} 
score  = 0
corruptLines = []

for l in lines:
    corruptChar = ''
    for c in l:
        if c in ['(', '[', '{','<']:
            stack.append(c)
        else:
            o = stack.pop()
            if not pairs[o] == c:
                corruptChar = c
                corruptLines.append(l)
                break
    if corruptChar:
        score += points[c]
    
print(f"Task 1: The score is {score}")

# Part 2
for l in corruptLines:
    lines.remove(l)

points = {')': 1, ']': 2, '}': 3, '>': 4} 
stack  = []
scores = []

for l in lines:
    completion = ''
    score = 0
    for c in l:
        if c in ['(', '[', '{','<']:
            stack.append(c)
        else:
            o = stack.pop()
    while stack:
        completion += pairs[stack.pop()]
    for c in completion:
        score *= 5
        score += points[c]
    scores.append(score)

scores.sort()

print(f"Task 2: The score is {scores[int(len(scores)/2)]}")
        
        
        