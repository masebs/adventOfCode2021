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

perms = list(range(3,10))
multipliers = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
targetscore = 21

cache = {}
cachehit = 0
cachemiss = 0

def playRec(startvals, startscores, p1turn):
    global cachemiss, cachehit
    wins = [0,0]
    vals = startvals.copy()
    scores = startscores.copy()
    i = 0 if p1turn else 1  # for some reason it won't work to simulate both players at once, so iterate between them
    for p in perms:
        vals[i] = (startvals[i] + p) % 10
        scores[i] = startscores[i] + vals[i]+1
        
        if scores[i] >= targetscore:
            wins[i] += 1 * multipliers[p]
        else:
            if (tuple(vals), tuple(scores), p1turn) not in cache:
                cachemiss += 1
                w = playRec(vals[:], scores[:], not p1turn)
                cache[(tuple(vals), tuple(scores), p1turn)] = w
            else:
                cachehit += 1
                w = cache[(tuple(vals), tuple(scores), p1turn)]
            wins[0] += w[0] * multipliers[p]
            wins[1] += w[1] * multipliers[p]
                
    return wins

wins = playRec([p1start-1, p2start-1], [0,0], True)

print(f"Task 2: Number of wins: {wins}")

