# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

# We definitely need a cache for reasonable runtime, so use tuples instead of lists in order to keep it hashable
grid = tuple([0 for _ in range(11)]) # represents only the hallway (1D)
roomPart1Test  = tuple([(1, 2), (4, 3), (3, 2), (1, 4)]) # Part 1 test data
roomPart1Input = tuple([(4, 2), (1, 2), (1, 3), (3, 4)]) # Part 1 input data
roomPart2Test  = tuple([(1, 4, 4, 2), (4, 2, 3, 3), (3, 1, 2, 2), (1, 3, 1, 4)]) # Part 2 test data
roomPart2Input = tuple([(4, 4, 4, 2), (1, 2, 3, 2), (1, 1, 2, 3), (3, 3, 1, 4)]) # Part 2 input data

home = {1: 2, 2: 4, 3: 6, 4: 8}
cost = {1: 1, 2: 10, 3: 100, 4: 1000}

# Returns a single minimum cost value, calculated recursively by trying all possibilities
def getCost(grid, room, roomsize, reclvl=0):
    global cachemiss, cachehit, cache
    possibleMotions = []        
        
    for idx, player in enumerate(grid): # for players in hallway: Those may only move into their home room!
        if player != 0 and len(room[player-1]) < roomsize \
                       and (len(room[player-1]) == 0 or all([room[player-1][k] == player for k in range(len(room[player-1]))])): 
            # we have an actual player, there is free space in his room and the lower space is either free or occupied
            #   by the right type of player (otherwise it is impossible or won't make sense to move in)
            length = roomsize - len(room[player-1]) # to move to the end of the room
            i = idx
            while i != home[player]:
                i = i-1 if home[player] < idx else i+1
                length += 1
                if grid[i] != 0:
                    break
            if i == home[player]:
                assert(idx >= 0)
                possibleMotions.append([player, idx, -1, length*cost[player]]) # -1 means: gone home
    # print("  pm hallway:", possibleMotions)
    
    for r in range(len(room)): # for players still in their starting rooms: come out to hallway 
        if len(room[r]) > 0 and (room[r][-1] != r+1 or \
                 (len(room[r]) >= 2 and any([room[r][k] != room[r][k-1] for k in range(1, len(room[r]))]) ) ):
            player = room[r][-1]
            idx = home[r+1]
            length = roomsize - len(room[r]) + 1
            while idx < len(grid)-1 and grid[idx+1] == 0: # go out and to the right
                idx += 1
                length += 1
                if idx not in home.values():
                    possibleMotions.append([player, -(r+1), idx, length*cost[player]]) # index negative -> player came out of room
            idx = home[r+1]
            length = roomsize - len(room[r]) + 1
            while idx > 0 and grid[idx-1] == 0: # go out and to the left
                idx -= 1
                length += 1
                if idx not in home.values():
                    possibleMotions.append([player, -(r+1), idx, length*cost[player]]) # index negative -> player came out of room
    # print("  pm out of rooms:", possibleMotions)
    
    if possibleMotions:
        costmin = 999999999
        pmopt = []
        plist = []
        for pm in possibleMotions: # first perform the motion on a copy of the grid and rooms, then recurse 
            if pm[1] >= 0: # player moving from hallway to target room
                roomcp = () # assembling the new room tuple is really annoying
                for r in range(len(room)):
                    if r == pm[0]-1:
                        filledRoom = ()
                        for pr in room[r]:
                            filledRoom += (pr,)
                        filledRoom += (pm[0],)
                        roomcp += (filledRoom,)
                    else:
                        roomcp += (room[r],)
                gridcp = tuple([(grid[i] if i != pm[1] else 0) for i in range(len(grid))])
            else:         # player moving out of start room
                player = room[abs(pm[1])-1][-1]
                roomcp = ()
                for r in range(len(room)):
                    if r == abs(pm[1])-1:
                        filledRoom = ()
                        for pr in room[r][:-1]:
                            filledRoom += (pr,)
                        roomcp += (filledRoom,)
                    else:
                        roomcp += (room[r],)
                gridcp = tuple([(grid[i] if i != pm[2] else pm[0]) for i in range(len(grid))])
            
            # print(gridcp)
            # print(roomcp)
            # print()
            
            if (gridcp, roomcp) in cache:
                pcost, plist = cache[(gridcp, roomcp)]
                cachehit += 1
            else:
                pcost, plist = getCost(gridcp, roomcp, roomsize, reclvl+1)
                cache[(gridcp, roomcp)] = (pcost, plist)
                cachemiss += 1
            newcost = pcost + pm[3]
            if newcost < costmin:
                costmin = newcost
                pmopt = plist + [pm]
            
        return costmin, pmopt
            
    else: # no more motions possible -> end of recursion
        if all([ room[i-1] == tuple([i for k in range(roomsize)]) for i in [1,2,3,4] ]): # success: everyone is in their rooms!
            # print("  found successful outcome at reclvl", reclvl)
            # print(grid)
            # print(room)
            return 0, [0]
        else: # no success and deadlock, return invalid cost
            # print("  deadlock")
            return 999999999, [-1]
    
### Execute Tasks
# room = roomPart1Test
room = roomPart1Input
roomsize = len(room[0])

cache = {}
cachemiss, cachehit = 0, 0

mincost, pmopt = getCost(grid, room, roomsize) 

print(f"\nTask 1: Minimum cost is {mincost}\n")
print(f"Task 1 optimum solution: {pmopt[:0:-1]}")

# room = roomPart2Test
room = roomPart2Input
roomsize = len(room[0])

cache = {}
cachemiss, cachehit = 0, 0

mincost, pmopt = getCost(grid, room, roomsize) 

print(f"\nTask 2: Minimum cost is {mincost}\n")
print(f"Task 2 optimum solution: {pmopt[:0:-1]}\n")
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    