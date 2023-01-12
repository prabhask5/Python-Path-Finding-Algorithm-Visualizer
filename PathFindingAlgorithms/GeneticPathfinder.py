import time
from GeneticAlgorithm.GeneticPopulation import GeneticPopulation
import pygame


def genetic(draw, start, end, came_from):
    pop = GeneticPopulation(100, start)
    genBeginTime = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        pop.update(start, end)
        if pop.allPlayersDead():
            genTime = time.time() - genBeginTime
            pop.naturalSelection(end)
            if pop.any_player_reached_goal and not pop.new_min_step:
                pop.reconstruct_path(start, came_from)
                draw()
                return True
            elif pop.gen > 100:
                if pop.any_player_reached_goal:
                    pop.reconstruct_path(start, came_from)
                    return True
                else:
                    return False
                draw()
                return pop.any_player_reached_goal
            else:
                pop.mutateChildren()
                genBeginTime = time.time()
        draw()
