from GeneticAlgorithm.GeneticPlayer import GeneticPlayer
import random


class GeneticPopulation():

    def __init__(self, size, initPos, path_length=1750):
        self.players = [GeneticPlayer(initPos, path_length)
                        for i in range(size)]
        self.gen = 1
        self.bestPlayer = None
        self.minStep = 200000
        self.new_min_step = False
        self.any_player_reached_goal = False
        self.fitnessSum = 0.0

    def update(self, start, end):
        for p in self.players:
            p.update(start, end)

    def calcFitness(self, end):
        for p in self.players:
            p.calculateFitness(end)

    def allPlayersDead(self):
        return all([p.dead or p.goal for p in self.players])

    def naturalSelection(self, end):
        self.new_min_step = False
        self.any_player_reached_goal = False
        newPlayers = [None for i in range(len(self.players))]
        self.calculateFitnessSum(end)
        bestPlayer = self.getBestPlayer()
        newPlayers[0] = self.players[bestPlayer].child()
        newPlayers[0].isBest = True
        for i in range(1, len((newPlayers))):
            parent = self.selectParent()
            newPlayers[i] = parent.child()
        self.players = newPlayers
        self.gen += 1

    def calculateFitnessSum(self, end):
        self.calcFitness(end)
        self.fitnessSum = sum([p.fitness for p in self.players])

    def selectParent(self):
        rand = random.random()
        runningSum = 0
        for p in sorted(self.players, key=lambda player: player.fitness, reverse=True):
            runningSum += (p.fitness)/(self.fitnessSum)
            if runningSum > rand:
                return p

    def mutateChildren(self):
        for i in range(1, len(self.players)):
            self.players[i].brain.mutate()

    def getBestPlayer(self):
        maxFit = 0
        maxIndex = 0
        for i in range(len(self.players)):
            if self.players[i].fitness > maxFit:
                maxFit = self.players[i].fitness
                maxIndex = i
        bestPlayer = maxIndex
        self.bestPlayer = self.players[bestPlayer]
        if self.players[bestPlayer].goal:
            self.any_player_reached_goal = True
            if self.players[bestPlayer].brain.step < self.minStep:
                self.new_min_step = True
                self.minStep = self.players[bestPlayer].brain.step
        return bestPlayer

    def reconstruct_path(self, start, came_from):
        best_path = self.players[0].brain.dir
        current = start
        for i in range(self.bestPlayer.brain.step):
            came_from[current] = current.neighbors[best_path[i]]
            current = current.neighbors[best_path[i]]
