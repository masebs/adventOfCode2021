# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

### Read input and split it into subprograms, each beginning with an "inp" command
with open("input-day24") as f:
    lines = f.readlines()
lines = [l.split() for l in lines]

linebuf = []
subprogs = []

for l in lines:
    if l == ['inp', 'w']:
        subprogs.append(linebuf)
        linebuf = []
        linebuf.append(l)
    else:
        linebuf.append(l)
subprogs.append(linebuf)
subprogs = subprogs[1:]

### Interpreter to run a program or subprogram
def runCode(lines, var, inpt):
    inpcounter = 0
    
    for l in lines:
        if l[0] == 'inp':
            var['w'] = int(inpt[inpcounter])
            inpcounter += 1
        elif l[0] == 'add':
            op1 = l[1]
            try: 
                op2 = int(l[2])
            except ValueError:
                op2 = l[2]
            if type(op2) == int: # add variable to variable
                var[op1] = var[op1] + op2
            else:
                var[op1] = var[op1] + var[op2]
            if l == ['add', 'z', 'y']:  # stop after each digit!
                break
        elif l[0] == 'mul':
            op1 = l[1]
            try: 
                op2 = int(l[2])
            except ValueError:
                op2 = l[2]
            if type(op2) == int: # add variable to variable
                var[op1] = var[op1] * op2
            else:
                var[op1] = var[op1] * var[op2]
        elif l[0] == 'div':
            op1 = l[1]
            try: 
                op2 = int(l[2])
            except ValueError:
                op2 = l[2]
            if type(op2) == int: # add variable to variable
                var[op1] = var[op1] // op2
            else:
                var[op1] = var[op1] // var[op2]    
        elif l[0] == 'mod':
            op1 = l[1]
            try: 
                op2 = int(l[2])
            except ValueError:
                op2 = l[2]
            if type(op2) == int: # add variable to variable
                var[op1] = var[op1] % op2
            else:
                var[op1] = var[op1] % var[op2]
        elif l[0] == 'eql':
            op1 = l[1]
            try: 
                op2 = int(l[2])
            except ValueError:
                op2 = l[2]
            if type(op2) == int: # add variable to variable
                var[op1] = int(var[op1] == op2)
            else:
                var[op1] = int(var[op1] == var[op2])
    
    return var
            

### Execute the subprograms in reverse order. Reasoning is: Each subprogram sets x and y to 0 at the beginning.
#   Therefore, the result of a subprogram only depends on the input and z. In the end, we need z = 0. Find all 
#   combinations of input number and z start value which lead to the desired z outcome. Then, set the z outcomes 
#   of the successful combinations as target z value for the next subprogram to be investigated (the previous one).
#   Do so until the first subprogram. The range of possible z values expands (going backwards) if the command
#   div z 26 is present, and it contracts if div z 1 is present instead. This can be used to limit the range of 
#   possible z start values to be investigated. More than 250000 is never required (found by trail-and-error) 
exponent = 0
inpt = list(range(1,10)) # the input numbers (1..10)
targetz = {0}  # z = 0 at the end means "accepted"
working = {}   # contains all values which meet the desired z outcome: [number input, z input, z outcome] 

for subp in range(len(subprogs)-1, -1, -1):
    print("Investigating subprogram", subp, "with targetz", targetz)
    var = {}
    var['x'] = 0 # x and y are set to 0 at the begin of each subprogram anyway, so it is save to set
    var['y'] = 0 #   them to 0 before starting the subprogram. z will be set below, w is set in the subprogram
    working[subp] = []
    
    if subprogs[subp][4] == ['div', 'z', '1']: # div z 1 is present: this subprogram requires a smaller z range 
        exponent -= 1
    elif subprogs[subp][4] == ['div', 'z', '26']: # div z 26 is present -> larger z range
        exponent += 1
        
    for z in list(range(0, min(26**exponent, 250000), 1)): # limit the input z as far as possible to save time
        for i in inpt:
            var['z'] = z
            inp = str(i)
            var = runCode(subprogs[subp], var, inp)
            if var['z'] in targetz:
                working[subp].append([i, z, var['z']])
    
    targetz = [w[1] for w in working[subp]]
    targetz = set(targetz)
    if not targetz: # This is if we haven't investigated enough z values somewhere in between
        print(f"Error in subprog {subp}: Empty target z!")
        break
    
### This goes through the working dictionary (recursively) and finds an accepted chain of input numbers
#   (accepted = it results in z value 0 in the end)
def getWorkingChain(working, subprog, zOutcome, searchMaximum=True):
    # print("subprog", subprog)
    if subprog >= len(subprogs):
        return [-1]
    workingWithZ = [w for w in working[subprog] if w[1] == zOutcome]
    workingnrs = sorted(workingWithZ, key = lambda w: w[0], reverse=searchMaximum)
    for w in workingnrs:
        nextres = getWorkingChain(working, subprog+1, w[2], searchMaximum)
        if nextres != []:
            nextres.append(w[0])
            # print("  found", w[0])
            return nextres
    # print("  found nuttin")
    return []

### Evaluate result for task 1 (find the largest accepted number for each digit)
reslist = getWorkingChain(working, 0, 0)
result = ''
while reslist:
    result += str(reslist.pop())
result = result[:-2]

print(f"\nTask 1: The maximum possible number is {result}")

### Execute evaluation for task 2 (the only difference is that the sort order in the function is reversed)
reslist = getWorkingChain(working, 0, 0, False)
result = ''
while reslist:
    result += str(reslist.pop())
result = result[:-2]

print(f"\nTask 2: The minimum possible number is {result}\n")
                  
            
            
            
            