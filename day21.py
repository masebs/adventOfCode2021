# -*- coding: utf-8 -*-
"""
Advent of Code 2021

@author marc 
"""

p1start = 9 # actual data
p2start = 4
# p1start = 4 # test data
# p2start = 8

dice  = [i for i in range(1,101)]
track = [i for i in range(1,10)]

def play(dicesize, targetpoints, startpos):
    score1 = 0
    score2 = 0
    dicecount = -1
    track1 = startpos[0]-1
    track2 = startpos[1]-1
    rolledcount = 0
    roundcount = 0
    
    while score1 < targetpoints and score2 < targetpoints:
        roundcount += 1
        dicevals = []
        for i in range(3): 
            dicecount = (dicecount + 1) % dicesize
            dicevals.append(dice[dicecount])
        rolledcount += 3
        track1 = (track1 + sum(dicevals)) % 10
        score1 += track1 + 1
        # print(f"Round {roundcount}: Player 1 rolls {dicevals} and moves to space {track1+1} for a total score of {score1}")
        
        if score1 >= targetpoints:
            p1Winning = True
            break
        
        dicevals = []
        for i in range(3): 
            dicecount = (dicecount + 1) % dicesize
            dicevals.append(dice[dicecount])
        rolledcount += 3
        track2 = (track2 + sum(dicevals)) % 10
        score2 += track2 + 1
        # print(f"Round {roundcount}: Player 2 rolls {dicevals} and moves to space {track2+1} for a total score of {score2}")
        
        if score2 >= targetpoints:
            p1Winning = False
            break
    return p1Winning, score1, score2, rolledcount 

p1Winning, score1, score2, rolledcount = play(100, 1000, (p1start, p2start))

print(f"\nPlayer {1 if p1Winning else 0} wins after {rolledcount} rolls, losing player has {score2 if p1Winning else score1} points,\
 result is {(score2 if p1Winning else score1)*rolledcount}\n")
 
dicevals = [(i,j, k) for i in [1,2,3] for j in [1,2,3] for k in [1,2,3]]
dicerolls = [(i,j) for i in dicevals for j in dicevals]
trackpos = [(i,j) for i in range(10) for j in range(10)]

# if we roll these dicevals at track positions tracks, we will end on tracks playSequence(dicevals, tracks)
def playSequence(dicevals, tracks): 
    tracks = ( (tracks[0] + sum(dicevals[0])) % 10, (tracks[1] + sum(dicevals[1])) % 10 )
    return tracks # score

seqs = {}
for tp in trackpos:
    for dr in dicerolls:
        seqs[(tp, dr)] = playSequence(dr, tp)
 
def playRec(targetpoints, scores, tpcounts, reclvl):
    
    if scores[0] >= targetpoints:
        return (1, 0)
    elif scores[1] >= targetpoints:
        return (0, 1)
    
    # do recursively until at bottom end of recursion target score is hit
    for tk in tpcounts.keys(): # e.g. pos 1x1, 5x2, 0x3, ...
        for dr in dicerolls:
            # recwins = playRec(targetpoints, scores, tk, reclvl+1)
            newtp = seqs[(tk, dr)]
            scores = (newtp[0]+1, newtp[1]+1)
            tpcounts[newtp] += 1
            wins = playRec(targetpoints, scores, tpcounts, reclvl+1)
        tpcounts[tk] -= 1
    
    if reclvl <= 3:
        print(f"on reclvl {reclvl}, score {scores}: {tpcounts}") 
        
    return tpcounts

    
tpcounts = {}
tpcounts[(p1start, p2start)] = 1
    
wins = playRec(21, (0, 0), tpcounts, 0)
 
 