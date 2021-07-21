from GeneticPlayer import GeneticPlayer
import pygame
from pygame.locals import *
import random

class GeneticPopulation():
    
    def __init__(self, size, movespeed, playersize, initPos, window, target, obsts, algo = 'set'):
        self.players = [GeneticPlayer(movespeed, playersize, initPos, algo) for i in range(size)]
        self.window = window
        self.targ = target
        self.obsts = obsts
        self.gen = 1
        self.bestPlayer = 0
        self.minStep = 200000
        self.fitnessSum = 0.0
            
    def update(self):
        for p in self.players:
            if p.brain.step > self.minStep:
                p.dead = True
            else:
                p.update(self.targ, self.window, self.obsts)

    def calcFitness(self):
        for p in self.players:
            p.calculateFitness(self.targ)
            
    def allPlayersDead(self):
        for p in self.players:
            if not p.dead and not p.reachedGoal:
                return False
        return True
    
    def naturalSelection(self):
        newPlayers = [None for i in range(len(self.players))]
        self.calculateFitnessSum()
        self.setBestPlayer()
        newPlayers[0] = self.players[self.bestPlayer].child()
        newPlayers[0].isBest = True
        for i in range(1, len((newPlayers))):
            parent = self.selectParent()
            newPlayers[i] = parent.child()
        for i in range(len(newPlayers)):
            self.players[i] = newPlayers[i]
        self.gen += 1
        
    def calculateFitnessSum(self):
        self.calcFitness()
        self.fitnessSum = 0
        for p in self.players:
            self.fitnessSum += p.fitness
            
    def selectParent(self):
        rand = random.random()
        runningSum = 0
        for p in self.players:
            runningSum += (p.fitness)/(self.fitnessSum)
            if runningSum > rand:
                return p
        return None
    
    def mutateChildren(self):
        for i in range(1, len(self.players)):
            self.players[i].brain.mutate()
            
    def setBestPlayer(self):
        maxFit = 0
        maxIndex = 0
        for i in range(len(self.players)):
            if self.players[i].fitness > maxFit:
                maxFit = self.players[i].fitness
                maxIndex = i
        self.bestPlayer = maxIndex
        if self.players[self.bestPlayer].reachedGoal:
            if self.players[self.bestPlayer].brain.step < self.minStep:
                print(f"New Shortest Path: {self.minStep} steps")
            self.minStep = self.players[self.bestPlayer].brain.step