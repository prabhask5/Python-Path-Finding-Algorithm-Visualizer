import pygame
from pygame.locals import *
import random

class GeneticProbBrain():
    def __init__(self):
        self.dir = self.randomize() # directions ordered by index: 0 Up, 1 Down, 2 Left, 3 Right
        self.step = 0
        
    def randomize(self):
        arr = [random.random() for i in range(4)]
        s = sum(arr)
        ret = [i/s for i in arr]
        return ret
    
    def clone(self):
        clone = GeneticProbBrain()
        for i in range(len(self.dir)):
            clone.dir[i] = self.dir[i]
        return clone
    
    def nextMove(self):
        rand = random.random()
        if rand <= self.dir[0]:
            return 0
        elif rand <= self.dir[0] + self.dir[1]:
            return 1
        elif rand <= self.dir[0] + self.dir[1] + self.dir[2]:
            return 2
        elif rand <= self.dir[0] + self.dir[1] + self.dir[2] + self.dir[3]:
            return 3
        
    def mutate(self): #Adds random amount (-0.05 to 0.05) to one prob and subtracts it from other
        choice = int((random.random()) * 4) #choosing which direction (U D L R) to mutate
        if choice == 4: #if we get very unlucky
            choice = 3
        mutationAmt = (random.random() / 10) - 0.05
        self.dir[choice] += mutationAmt
        choice = int((random.random()) * 4) #choosing which direction (U D L R) to compensate for mutation
        if choice == 4: #if we get very unlucky
            choice = 3
        self.dir[choice] -= mutationAmt