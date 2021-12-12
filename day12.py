# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

with open("input-day12", 'r') as f:
# with open("input-day12-test2", 'r') as f:
    lines = [l.split()[0] for l in f.readlines()]

graph = {}
for l in lines:
    try: # add forwards connection
        graph[l.split('-')[0]].append(l.split('-')[1]) 
    except KeyError:
        graph[l.split('-')[0]] = [l.split('-')[1]]
    try: # add backwards connection
        graph[l.split('-')[1]].append(l.split('-')[0]) 
    except KeyError:
        graph[l.split('-')[1]] = [l.split('-')[0]]

pathcount = 0

def trace(graph, node, nodelist=[]):
    global pathcount
    # print('Entering node', node, "on path", nodelist)
    nodelist = nodelist.copy()
    nodelist.append(node)
    
    if node == 'end':
        pathcount += 1
        # print(f"Found path: {nodelist}")
        return
    else:
        neighbors = [n for n in graph[node] if (n.isupper() or n not in nodelist) and n != 'start']
        # print("   neighbors:",  neighbors)
        
        for n in neighbors:
            trace(graph, n, nodelist)
    
trace(graph, 'start')

print()
print(f"Task 1: Found {pathcount} paths")   
print()     

pathcount = 0

def trace2(graph, node, nodelist=[], usedJoker=False, reclvl=0):
    global pathcount
    nodelist = nodelist.copy()
    nodelist.append(node)
    
    if node == 'end':
        pathcount += 1
        # print(f"Found path: {nodelist}, recursion level {reclvl}")
        return
    else:
        neighbors = [n for n in graph[node] if (n.isupper() or n not in nodelist) and n != 'start']
        jokers = []
        if not usedJoker: 
            allneighbors = [n for n in graph[node] if n != 'start']
            jokers = [n for n in allneighbors if n not in neighbors]
        
        for n in neighbors:
            trace2(graph, n, nodelist, usedJoker, reclvl+1)
        for j in jokers:
            trace2(graph, j, nodelist, True, reclvl+1)

trace2(graph, 'start')

#print()
print(f"Task 2: Found {pathcount} paths")     
        
        