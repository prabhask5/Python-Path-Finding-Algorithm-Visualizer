import random


class GeneticSetBrain():

    def __init__(self, path_length):
        # directions given by element number: 0 Up, 1 Down, 2 Left, 3 Right
        self.dir = self.randomize(path_length)
        self.path_length = path_length
        self.step = 0

    def randomize(self, size):
        ret = [random.randint(0, 3) for i in range(size)]
        return ret

    def clone(self):
        clone = GeneticSetBrain(self.path_length)
        for i in range(len(self.dir)):
            clone.dir[i] = self.dir[i]
        return clone

    def get_next_move(self):
        if self.step < len(self.dir):
            move = self.dir[self.step]
            self.step += 1
            return move

    def can_move(self):
        return self.step < len(self.dir)

    def mutate(self):
        baseMutRate = 0.01
        maxMutRate = 0.25
        for i in range(len(self.dir)):
            rand = random.random()
            if rand < (i/len(self.dir)) * (maxMutRate - baseMutRate) + baseMutRate:
                self.dir[i] = random.randint(0, 3)
