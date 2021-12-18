# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

from json import loads

with open("input-day18", 'r') as f:
# with open("input-day18-test1", 'r') as f:
# with open("input-day18-test2", 'r') as f:
# with open("input-day18-test3", 'r') as f:
    lines = f.readlines()

nbrs = [loads(l.split()[0]) for l in lines]
# nbrs = [nbrs[0], nbrs[1]]

def explode(nr): # the explode mechanism by string replacement
    strnr = str(nr).replace(' ', '')
    bracketstack = []
    allstack     = []
    toBeExploded = []
    changed = False
    for k, c in enumerate(strnr):
        allstack.append((c, k))
        if c == '[':
            bracketstack.append(c)
            if len(bracketstack) == 5:
                substr = ''
                j = k+1
                sc = strnr[j]
                while sc != ']':
                    substr += sc
                    j += 1
                    sc = strnr[j]
                # print("substr", substr)
                toBeExploded = substr.split(',')
                # print ("toBeExploded", toBeExploded, j)
                
                newstr = strnr[:k] + '0' + strnr[j+1:]
                
                i = k-1
                sc = newstr[i]
                while sc in '[],' and 0 < i: # find last number
                    i -= 1
                    sc = newstr[i]
                replaceEnd = i+1
                while sc in '0123456789' and 0 < i:
                    i -= 1
                    sc = newstr[i]
                replaceStart = i+1
                if 0 < i:
                    # print("last: rs, re: ", replaceStart, replaceEnd, newstr[:replaceStart], str(int(toBeExploded[0])+int(newstr[replaceStart:replaceEnd])), newstr[replaceEnd:])
                    # print(f"Replacing {newstr[replaceStart:replaceEnd]} by {str(int(toBeExploded[0])+int(newstr[replaceStart:replaceEnd]))}")
                    newstr = newstr[:replaceStart] + str(int(toBeExploded[0])+int(newstr[replaceStart:replaceEnd])) + newstr[replaceEnd:]
                    
                i = k+2
                sc = newstr[i]
                while sc in '[],' and i < len(newstr)-1: # find next number
                    i += 1
                    sc = newstr[i]
                replaceStart = i
                while sc in '0123456789' and i < len(newstr)-1:
                    i += 1
                    sc = newstr[i]
                replaceEnd = i
                if i < len(newstr)-1:
                    # print("next: rs, re: ", replaceStart, replaceEnd, newstr[:replaceStart], str(int(toBeExploded[1])+int(newstr[replaceStart:replaceEnd])), newstr[replaceEnd:])
                    # print(f"Replacing {newstr[replaceStart:replaceEnd]} by {str(int(toBeExploded[1])+int(newstr[replaceStart:replaceEnd]))}")
                    newstr = newstr[:replaceStart] + str(int(toBeExploded[1])+int(newstr[replaceStart:replaceEnd])) + newstr[replaceEnd:]
                    
                strnr = newstr
                # print("  exploded:", strnr)
                changed = True
                break
            
        elif c == ']':
            cp = bracketstack.pop()
            assert(cp == '[')
        
    if changed == False:
        return loads(strnr), False
    else:
        # print("  explode returning:", strnr)
        return explode(loads(strnr))[0], True # do recursively until nothing changes any more

def split(nr): # split mechanism by string replacement
    strnr = str(nr).replace(' ','')
    stack = []
    changed = False
    for k, c in enumerate(strnr):
        if c in '0123456789' and stack[-1] in '0123456789':
            strnr = strnr[:k-1] + '[' + str(int(stack[-1]+c)//2) + ',' + str(int(stack[-1]+c)-int(stack[-1]+c)//2) + ']' + strnr[k+1:]
            changed = True
            break
        else:
            stack.append(c)
    # print("  split returning:  ", strnr)
    return loads(strnr), changed

def reduce(nr): # reduce -> explode and split until nothing changes any more
    changed = True
    while changed:
        nr, changed = explode(nr)
        nr, changed = split(nr)
        # print(nr)
    return nr
    
def add(left, right): 
    return [left, right]

class Node:  # Tree for obtaining magnitude
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.value = None
    
def magnitude(nr): # obtain magnitude by building a tree and doing post-order traversal
    strnr = str(nr).replace(' ','')
    root = Node()
    tree = root
    preread = 0
    for k, c in enumerate(strnr):
        if preread > 0:
            preread -= 1
            continue
        # print("Stack: ", stack)
        if c == '[':
            # print("go left")
            tree.left = Node()
            old = tree
            tree = tree.left
            tree.parent = old
        elif c in '0123456789':
            j = k
            n = strnr[j]
            while n in '0123456789':
                j += 1
                n = strnr[j]
            tree.value = int(strnr[k:j])
            preread = j-k-1
            # print("leaf: value", tree.value)
        elif c == ',':
            # print("go to right brother")
            tree = tree.parent
            tree.right = Node()
            old = tree
            tree = tree.right
            tree.parent = old
        elif c == ']':
            # print("go up")
            tree = tree.parent
    return postorder(tree)
            
def postorder(tree): 
    if tree.value != None:
        return tree.value
    else:
        return 3*postorder(tree.left) + 2*postorder(tree.right)
    
            
res = nbrs[0]

for n in nbrs[1:]:
    add1 = res
    # print("add1:", add1)
    add2 = n
    # print("add2:", add2)
    added = add(add1, add2)
    # print("added:", str(added).replace(' ', ''))
    res = reduce(added)
    # print("res:", str(res).replace(' ', ''))
    
mag = magnitude(res)
print(f"Task 1: Magnitude is {mag}, result = {res}")

perm = [(i,j) for i in range(len(nbrs)) for j in range(len(nbrs))]
perm = [p for p in perm if p[0] != p[1]]

maxmag = 0

for p in perm:
    # print(p)
    mag = magnitude(reduce(add(nbrs[p[0]], nbrs[p[1]])))
    if mag > maxmag:
        maxmag = mag

print(f"Task 2: Maximum sum magnitude {maxmag}")
    

