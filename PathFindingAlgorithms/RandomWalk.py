import pygame
import random


def random_walk(draw, start, end, came_from, max_steps=10000):
    walk = [start]
    steps = 0
    while len(walk) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
        current_node = walk.pop()
        if current_node is not start and current_node is not end:
            current_node.make_on_current_path()
        steps += 1
        if steps == max_steps:
            return False
        elif current_node is end:
            return True
        next_node = random.choice(
            [neighbor for neighbor in current_node.neighbors if neighbor])
        if next_node.is_on_current_path() or next_node.is_start():
            previous_node = current_node
            while previous_node is not next_node and previous_node is not start:
                if previous_node is not start and previous_node is not end:
                    previous_node.reset()
                copy_of_prev_node = previous_node
                previous_node = came_from[previous_node]
                del came_from[copy_of_prev_node]
        else:
            came_from[next_node] = current_node
        walk.append(next_node)
        draw()
    return False
