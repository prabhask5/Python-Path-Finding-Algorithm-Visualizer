import pygame
from collections import deque


def dfs(draw, start, end, came_from, is_progressive_generation):
    open_set = deque()
    open_set.append(start)
    closed_set = []

    while len(open_set) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        current = open_set.pop()

        if current not in closed_set:
            if current is end:
                return True

            for neighbor in [neighbor for neighbor in current.neighbors if neighbor is not None]:
                if neighbor not in closed_set:
                    came_from[neighbor] = current
                    open_set.append(neighbor)
                    if neighbor is not start and neighbor is not end:
                        neighbor.make_open()
            if is_progressive_generation:
                draw()

            if current is not start and current is not end:
                current.make_closed()
            closed_set.append(current)

    return False
