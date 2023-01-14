import pygame
from queue import Queue


def bidirectional_bfs(draw, start, end, came_from_start, came_from_end):
    open_set_start = Queue()
    open_set_end = Queue()
    open_set_start.put(start)
    open_set_end.put(end)
    closed_set_start = []
    closed_set_end = []

    while open_set_start.qsize() > 0 and open_set_end.qsize() > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        current_start_side = open_set_start.get()
        current_end_side = open_set_end.get()

        if current_start_side not in closed_set_start:
            if current_start_side in closed_set_end:
                return True, current_start_side

            for neighbor in [neighbor for neighbor in current_start_side.neighbors if neighbor is not None]:
                if neighbor not in closed_set_start:
                    came_from_start[neighbor] = current_start_side
                    open_set_start.put(neighbor)
                    if not neighbor.is_closed_secondary() and neighbor is not start and neighbor is not end:
                        neighbor.make_open()

            if current_start_side is not start and current_start_side is not end:
                current_start_side.make_closed()
            closed_set_start.append(current_start_side)

        if current_end_side not in closed_set_end:
            if current_end_side in closed_set_start:
                return True, current_end_side

            for neighbor in [neighbor for neighbor in current_end_side.neighbors if neighbor is not None]:
                if neighbor not in closed_set_end:
                    came_from_end[neighbor] = current_end_side
                    open_set_end.put(neighbor)
                    if not neighbor.is_closed() and neighbor is not start and neighbor is not end:
                        neighbor.make_open_secondary()

            if current_end_side is not end and current_end_side is not start:
                current_end_side.make_closed_secondary()
            closed_set_end.append(current_end_side)

        draw()

    return False, None
