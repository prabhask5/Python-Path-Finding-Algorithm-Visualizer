import pygame
from pygame.locals import *
import random

class GeneticSetBrain():
    
    def __init__(self):
        self.dir = self.randomize(4000) # directions given by element number: 0 Up, 1 Down, 2 Left, 3 Right
        self.step = 0
        
    
    def randomize(self, size):
        ret = [random.randint(0, 3) for i in range(size)]
        return ret
    
    def clone(self):
        clone = GeneticSetBrain()
        for i in range(len(self.dir)):
            clone.dir[i] = self.dir[i]
        return clone
    
    def nextMove(self):
        return self.dir[self.step]
        
    def mutate(self):
        baseMutRate = 0.01
        maxMutRate = 0.25
        for i in range(len(self.dir)):
            rand = random.random()
            if rand < (i/len(self.dir)) * (maxMutRate - baseMutRate) + baseMutRate:
                self.dir[i] = random.randint(0, 3)