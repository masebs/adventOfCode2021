# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

with open("input-day20", 'r') as f:
# with open("input-day20-test", 'r') as f:
    lines = f.readlines()
algo = [1 if c == '#' else 0 for c in lines[0].split()[0]]
image = [[1 if c == '#' else 0 for c in l.split()[0]] for l in lines[2:]]
image = np.array(image, dtype=int)

def enlargeImage(image, nstep):
    margin = 6
    size = image.shape[0] + margin # add border on all sides
    if nstep % 2 == 1: # account for blinking infinite surroundings
        newimg = np.ones((size, size), dtype=int)
    else:
        newimg = np.zeros((size, size), dtype=int)
    newimg[margin//2:size-margin//2, margin//2:size-margin//2] = image
    return newimg

def printImg(image):
    for line in image:
        l = ''
        for c in line:
            l += '#' if c == 1 else '.'
        print(l)
    print()

nsteps = 50

def solve(image, algo, nsteps):
    for k in range(nsteps):
        print(k)
        if algo[0] == 1: # empty part of image blinks (if algo[-1] == 0, which is the case for the input)
            image = enlargeImage(image, k)
        else:
            image = enlargeImage(image, 0)
        idcs = np.where(image==1)
        evalimg = np.zeros(image.shape, dtype=int)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                idcs = [(m,n) for m in range(i-1,i+2) for n in range(j-1,j+2)]
                evalstr = ''
                for idx in idcs:
                    if 0 <= idx[0] < image.shape[0] and 0 <= idx[1] < image.shape[1]:
                        evalstr += str(image[idx])
                    else:
                        if algo[0] == 1 and k % 2 == 1:
                            evalstr += '1'
                        else:
                            evalstr += '0'
                evalimg[i,j] = int(evalstr, 2)
        
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i,j] = algo[evalimg[i,j]]        
        if nsteps < 5:
            printImg(image)
    return np.where(image == 1)[0].shape[0]

count = solve(image.copy(), algo, 2)
print(f"Task 1: {count} pixels are lit")

count = solve(image.copy(), algo, 50)
print(f"Task 2: {count} pixels are lit")
