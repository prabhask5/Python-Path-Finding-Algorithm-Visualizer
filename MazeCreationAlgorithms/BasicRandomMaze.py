import random


def generate_random_maze(grid, prob_gen_wall=0.25):
    for row in grid:
        for spot in row:
            val = random.random()
            if val < prob_gen_wall:
                spot.make_barrier()
