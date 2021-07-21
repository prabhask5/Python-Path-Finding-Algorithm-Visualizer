import GeneticPopulation
import pygame
from pygame.locals import *
import random

def genetic(player, targ, obsts, myWindow, moveSpeed, popSize):
    playerSize = abs(player.right - player.left)
    initPos = (player.left, player.top)
    myPop = GeneticPopulation(popSize, moveSpeed, playerSize, initPos, myWindow, targ, obsts, 'set')
    
    streak = 0
    bestFitness = 0
    while streak < 100:
        newBest = myPop.players[myPop.bestPlayer].fitness
        if bestFitness == newBest:
            streak += 1
        else:
            streak = 0
            bestFitness = newBest
        
        while not myPop.allPlayersDead():
            myPop.update()
        
        myPop.naturalSelection()
        myPop.mutateChildren()
    
    optimalDir = myPop.players[myPop.bestPlayer].brain.dir
    optimalPath = [(player.centerx, player.centery)]
    for i in range(len(optimalDir)):
        oldSpot = optimalPath[-1]
        newDir = optimalDir[i]
        if newDir == 0:
            move = (0, 1)
        if newDir == 1:
            move = (0, -1)
        if newDir == 2:
            move = (-1, 0)
        if newDir == 3:
            move = (1, 0)
        newSpot = (oldSpot[0] + move[0], oldSpot[1] + move[1])
        optimalPath.append(newSpot)
    return optimalPath
        
        