import random
import pygame
from pygame.locals import *
from GeneticProbBrain import GeneticProbBrain
from GeneticSetBrain import GeneticSetBrain

class GeneticPlayer():
    def __init__(self, moveSpeed, playerSize, initPos, algo):
        self.moveSpeed = moveSpeed
        self.playerSize = playerSize
        self.initPos = initPos
        self.algo = algo
        self.player = pygame.Rect(initPos[0], initPos[1], playerSize, playerSize)
        if algo == 'prob':
            self.brain = GeneticProbBrain()
        else:
            self.brain = GeneticSetBrain()
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0.0
           
    def move(self):
        direction = self.brain.nextMove()
        self.brain.step += 1
        v = [self.moveSpeed, self.moveSpeed]
        if direction == 2:
            v[0] *= -1
            v[1] *= 0
        if direction == 3:
            v[0] *= 1
            v[1] *= 0
        if direction == 0:
            v[0] *= 0
            v[1] *= 1
        if direction == 1:
            v[0] *= 0
            v[1] *= -1
        self.player.centerx += v[0]
        self.player.centery += v[1]
        
    def update(self, targ, window, obsts):
        windRect = window
        if not self.dead and not self.reachedGoal:
            self.move()
            if self.player.colliderect(targ):
                self.reachedGoal = True
            elif not windRect.contains(self.player):
                self.dead = True
            else:
                collision = False
                for obst in obsts:
                    if self.player.colliderect(obst):
                        collision = True
                if collision:
                    self.dead = True
                    
    def calculateFitness(self, targ):
        if self.reachedGoal:
            self.fitness = 10 + 10/(self.brain.step * self.brain.step)
        else:
            distanceToGoal = ((self.player.centerx - targ.centerx)**2 + (self.player.centery - targ.centery)**2)**(1/2)
            self.fitness = 10/(distanceToGoal * distanceToGoal)
            
    def child(self):
        baby = GeneticPlayer(self.moveSpeed, self.playerSize, self.initPos, self.algo)
        baby.brain = self.brain.clone()
        return baby