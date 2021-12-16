# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""


# hexinp = 'D2FE28'
# hexinp = '38006F45291200'
# hexinp = 'EE00D40C823060'
hexinp = '8A004A801A8002F478'
# hexinp = '620080001611562C8802118E34'
# hexinp = 'C0015000016115A2E0802F182340'
# hexinp = 'A0016C880162017C3686B18A3D4780'

# with open("input-day16", 'r') as f:
# # with open("input-day16-test", 'r') as f:
#     hexinp = f.readlines()[0].split()

dezval = int(hexinp, 16)
binval = bin(dezval)
strval = str(binval)[2:]

versionsum = 0

def getPacketLength(strval):
    version = int(strval[:3], 2)
    # print(" version:", version)
    versionsum += version
    typeid  = int(strval[3:6], 2)
    # print(" typeid:", typeid)
    length = 6
    if typeid == 4:
        for k in range(6, len(strval), 5):
            packagefollows = int(strval[k], 2)
            length += 5
            if packagefollows == 0:
                break
        print("   found literal length", length)
        return length
    else:
        lengthtype = int(strval[6], 2)
        # print(" lengthtype:", lengthtype)
        if lengthtype == 0:
            totallength = int(strval[7:20], 2)
            length += 20 + totallength
            print("   found operator type 0 length", length)
        else:
            nrpacks = int(strval[7:18], 2)
            print(" nrpacks:", nrpacks)
            k = 18
            for n in range(nrpacks):
                substr = strval[k:], 2
                length += getPacketLength(substr)
            print("   found operator type 1 length", length)
        
def decodePacket(strval):
    global versionsum
    
    version = int(strval[:3], 2)
    print(" version:", version)
    versionsum += version
    typeid  = int(strval[3:6], 2)
    print(" typeid:", typeid)
    if typeid == 4:
        literal = ''
        for k in range(6, len(strval), 5):
            packagefollows = int(strval[k], 2)
            literal += strval[k+1:k+5]
            if packagefollows == 0:
                break
        literal= int(literal, 2)
        print(" literal:", literal)
    else: # we've got an operator
        lengthtype = int(strval[6], 2)
        print(" lengthtype:", lengthtype)
        subpack = ''
        if lengthtype == 0:
            totallength = int(strval[7:20], 2)
            print(" totallength:", totallength)
            k = 20
            while k-19 < totallength:
                packagefollows = 1
                endidx = k+6
                while packagefollows:
                    packagefollows = int(strval[endidx], 2)
                    endidx += 5
                subpack = strval[k:endidx]
                print("decoding subpacket:", subpack)
                decodePacket(subpack)
                k = endidx 
                
        else:
            nrpacks = int(strval[7:18], 2)
            print(" nrpacks:", nrpacks)
            k = 18
            for n in range(nrpacks):
                subpacktype = int(strval[k+3:k+6], 2)
                print(" subpacktype:", subpacktype)
                if subpacktype == 4: # subpack is literal
                    packagefollows = 1
                    endidx = k+6
                    while packagefollows:
                        packagefollows = int(strval[endidx], 2)
                        endidx += 5 
                    subpack = strval[k:endidx]
                else: # subpack is operator package
                    suboptype = int(strval[k+6], 2)
                    print(" suboptype:", suboptype)
                    if suboptype == 0:
                        suboplength = int(strval[k+7:k+22])
                        subpack = strval[k:k+22+suboplength]
                    else:
                        suboppacknr = int(strval[k+7:k+18])
                        packagefollows = 1
                        endidx = k+18
                        while packagefollows:
                            packagefollows = int(strval[endidx], 2)
                            endidx += 5 
                        suboplength = suboppacknr * (endidx - (k+18))
                        subpack = strval[k:k+18+suboplength]
                            
                    
                print(f"decoding subpacket: {subpack}")
                decodePacket(subpack)
                k = endidx
        
decodePacket(strval)

print(f"Task 1: Sum of versions is {versionsum}")

