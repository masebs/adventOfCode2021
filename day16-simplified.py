# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

import numpy as np

### Test data
# Part 1
# hexinp = 'D2FE28'
# hexinp = '38006F45291200'
# hexinp = 'EE00D40C823060'
# hexinp = '8A004A801A8002F478'
# hexinp = '620080001611562C8802118E34'
# hexinp = 'C0015000016115A2E0802F182340'
# hexinp = 'A0016C880162017C3686B18A3D4780'

# Part 2
# hexinp = 'C200B40A82'
# hexinp = '04005AC33890'
# hexinp = '880086C3E88112'
# hexinp = 'CE00C43D881120'
# hexinp = 'D8005AC2A8F0'
# hexinp = 'F600BC2D8F'
# hexinp = '9C005AC2F8F0'
# hexinp = '9C0141080250320F1802104A08'


with open("input-day16", 'r') as f:
# #with open("input-day16-test", 'r') as f:
    hexinp = f.readlines()[0].split()[0]

def printIfVerbose(s): # for logging
    global verbose
    if verbose:
        print(s)

verbose = False

dezval = int(hexinp, 16)
binval = bin(dezval)
strval = str(binval)[2:] # the binary string to be processed

requiredlength = len(hexinp)*4 # pad leading zeros in case they are missing
missingZeros = requiredlength - len(strval)
padstring = ''
while missingZeros:
    padstring += '0'
    missingZeros -= 1
strval = padstring + strval

versionsum = 0 # result for part 1

def decodePacket(strval):
    global versionsum
    printIfVerbose(f"Decoding {strval}")
        
    version = int(strval[:3], 2)
    versionsum += version
    typeid  = int(strval[3:6], 2)
    printIfVerbose(f" version: {version}")
    printIfVerbose(f" typeid: {typeid}")
    lengthread = 6
    
    if typeid == 4:
        literal = ''
        for k in range(6, len(strval), 5):
            packagefollows = int(strval[k], 2)
            literal += strval[k+1:k+5]
            lengthread += 5
            if packagefollows == 0:
                break
        literal = int(literal, 2)
        printIfVerbose(f" literal: {literal}")
        return literal, lengthread
    
    else: # we've got an operator
        operands = []
        lengthtype = int(strval[6], 2)
        printIfVerbose(f" lengthtype: {lengthtype}")
        
        if lengthtype == 0:
            totallength = int(strval[7:22], 2)
            k = 22
            lengthread += 16
            while k < 22 + totallength:
                op, length = decodePacket(strval[k:])
                operands.append(op)
                k += length
                lengthread += length
                
        else:
            nrpacks = int(strval[7:18], 2)
            k = 18
            lengthread += 12
            for n in range(nrpacks):
                op, length = decodePacket(strval[k:])
                operands.append(op)
                k += length
                lengthread += length
                
        printIfVerbose(f"Operands: {operands}")
        
        if typeid == 0:
            return sum(operands), lengthread
        elif typeid == 1:
            return np.product(operands), lengthread
        elif typeid == 2:
            return np.min(operands), lengthread
        elif typeid == 3:
            return np.max(operands), lengthread
        elif typeid == 5:
            return int(operands[0] > operands[1]), lengthread
        elif typeid == 6:
            return int(operands[0] < operands[1]), lengthread
        elif typeid == 7:
            return int(operands[0] == operands[1]), lengthread
        else:    
            return -1, lengthread

result, _ = decodePacket(strval)

print(f"\nTask 1: Sum of versions is {versionsum}")
print(f"Task 2: Result is {result}")
