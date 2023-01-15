import pygame
import random


def generate_simple_stair(draw, grid):
    current = grid[random.randint(0, len(grid) - 1)][0]
    dir = True  # true is up, false is down

    while current:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
        if current.true_col >= len(grid[0]) - 1:
            current = None
        else:
            current.make_barrier()
            if dir:
                if current.row <= 1:
                    dir = not dir
                else:
                    current = grid[current.row - 1][current.true_col + 1]
            else:
                if current.row >= len(grid) - 2:
                    dir = not dir
                else:
                    current = grid[current.row + 1][current.true_col + 1]
            draw()
