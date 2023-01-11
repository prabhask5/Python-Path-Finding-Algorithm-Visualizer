from GeneticAlgorithm.GeneticSetBrain import GeneticSetBrain


class GeneticPlayer():
    def __init__(self, initPos, path_length):
        self.initPos = initPos
        self.pos = initPos
        self.brain = GeneticSetBrain(path_length)
        self.dead = False
        self.goal = False
        self.isBest = False
        self.fitness = 0.0

    def move(self, start):
        self.pos.reset()
        if self.pos is start:
            start.make_start()
        dir = self.brain.get_next_move()
        new_pos = self.pos.neighbors[dir]
        if new_pos is None:
            self.dead = True
            return
        else:
            self.pos = new_pos
        if self.isBest:
            self.pos.make_best()
        else:
            if not self.pos.is_best():
                self.pos.make_genetic_player()

    def update(self, start, end):
        if not self.dead and not self.goal:
            self.move(start)
            if self.dead:
                return
            elif self.pos is end:
                self.goal = True
                self.pos.make_end()
            elif not self.brain.can_move():
                self.dead = True
                if self.pos is start:
                    self.pos.make_start()
                else:
                    self.pos.reset()

    def calculateFitness(self, end):
        if self.goal:
            self.fitness = 10 + 10/(self.brain.step * self.brain.step)
        else:
            x1, y1 = self.pos.get_pos()
            x2, y2 = end.get_pos()
            distanceToGoal = ((x2 - x1)
                              ** 2 + (y2 - y1)**2)**(1/2)
            self.fitness = 10/(distanceToGoal * distanceToGoal)

    def child(self):
        baby = GeneticPlayer(self.initPos, self.brain.path_length)
        baby.brain = self.brain.clone()
        return baby
