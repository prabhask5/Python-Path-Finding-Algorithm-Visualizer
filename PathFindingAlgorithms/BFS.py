import pygame
from queue import Queue


def bfs(draw, start, end, came_from):
    open_set = Queue()
    open_set.put(start)
    closed_set = []

    while open_set.qsize() > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        current = open_set.get()

        if current not in closed_set:
            if current is end:
                return True

            for neighbor in [neighbor for neighbor in current.neighbors if neighbor is not None]:
                if neighbor not in closed_set:
                    came_from[neighbor] = current
                    open_set.put(neighbor)
                    neighbor.make_open()
            draw()

            if current is not start:
                current.make_closed()
            closed_set.append(current)

    return False
