# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

### Attempt with trees - should be a lot simpler, but is not yet working

# with open("input-day18", 'r') as f:
with open("input-day18-test1", 'r') as f:
# with open("input-day18-test2", 'r') as f:
# with open("input-day18-test3", 'r') as f:
    lines = f.readlines()

nbrs = [loads(l.split()[0]) for l in lines]
# nbrs = [nbrs[0], nbrs[1]]

def explode(tree): # the explode mechanism in a tree
    low = findLow(tree, 0)
    if low != None:
        changed = True
    else:
        changed = False
    while low != None:
        print(low.left.value, low.right.value)
        leftnbr = low.parent
        while leftnbr.right != None:
            leftnbr = leftnbr.right
        rightnbr = low.parent
        while rightnbr.left != None:
            rightnbr = rightnbr.left
        leftnbr.value += low.left.value
        rightnbr.value += low.right.value
        low.value = 0
        low.left = None
        low.right = None
        low = findLow(tree, 0)
    return tree, changed

def findLow(tree, level):
    if tree.left != None and tree.right != None:
        print(level, tree.left.value, tree.right.value)
        if level == 4:
                return tree
        else:
            leftres = findLow(tree.left, level+1)
            if leftres != None:
                return leftres 
            else:
                rightres = findLow(tree.right, level+1)
                if rightres != None:
                    return rightres 
                else: 
                    return None
                
    else:
        return None
           
def split(tree): # split mechanism in tree
    largeNode = findLarge(tree)
    if largeNode == None:
        changed = False
    else: 
        changed = True
        largeNode.left = Node()
        largeNode.left.value = largeNode.value // 2
        largeNode.right.value = largeNode.value // 2 + 1
        largeNode.value = None
        largeNode.left.parent = largeNode
        largeNode.right.paren = largeNode
    return tree, changed

def findLarge(tree):
    if tree.value != None:
        if tree.value >= 10:
            return tree
        else:
            return None
    else:
        leftval = findLarge(tree.left)
        if leftval != None:
            return leftval
        else:
            rightval = findLarge(tree.right)
            if rightval != None:
                return rightval
            else:
                return None
            
    
def reduce(tree): # reduce -> explode and split until nothing changes any more
    changed = True
    while changed:
        tree, changed = explode(tree)
        tree, changed = split(tree)
        # print(nr)
    return tree
    
def add(left, right): 
    tree = Node()
    tree.left = left 
    tree.right = right 
    tree.left.parent = tree
    tree.right.parent = tree
    return tree

class Node:  # Tree for obtaining magnitude
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.value = None
    
def buildTree(nr): # obtain magnitude by building a tree and doing post-order traversal
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
    return tree 

def magnitude(tree): 
    if tree.value != None:
        return tree.value
    else:
        return 3*magnitude(tree.left) + 2*magnitude(tree.right)
    
            
res = buildTree(nbrs[0])

for n in nbrs[1:]:
    add1 = res
    # print("add1:", add1)
    add2 = buildTree(n)
    # print("add2:", add2)
    added = add(add1, add2)
    # print("added:", str(added).replace(' ', ''))
    res = reduce(added)
    # print("res:", str(res).replace(' ', ''))
    
mag = magnitude(res)
print(f"Task 1: Magnitude is {mag}, result = {res}")

# perm = [(i,j) for i in range(len(nbrs)) for j in range(len(nbrs))]
# perm = [p for p in perm if p[0] != p[1]]

# maxmag = 0

# for p in perm:
#     # print(p)
#     mag = magnitude(reduce(add(nbrs[p[0]], nbrs[p[1]])))
#     if mag > maxmag:
#         maxmag = mag

# print(f"Task 2: Maximum sum magnitude {maxmag}")
    

