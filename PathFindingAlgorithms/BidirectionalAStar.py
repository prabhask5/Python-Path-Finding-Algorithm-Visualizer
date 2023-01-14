import pygame
from queue import PriorityQueue


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def bidirectional_astar(draw, grid, start, end, came_from_start, came_from_end):
    count_start = 0
    count_end = 0
    open_set_start = PriorityQueue()
    open_set_start.put((0, count_start, start))
    open_set_end = PriorityQueue()
    open_set_end.put((0, count_end, end))
    g_score_start = {spot: float("inf") for row in grid for spot in row}
    g_score_start[start] = 0
    g_score_end = {spot: float("inf") for row in grid for spot in row}
    g_score_end[end] = 0
    f_score_start = {spot: float("inf") for row in grid for spot in row}
    f_score_start[start] = h(start.get_pos(), end.get_pos())
    f_score_end = {spot: float("inf") for row in grid for spot in row}
    f_score_end[end] = h(end.get_pos(), start.get_pos())
    closed_set_start = []
    closed_set_end = []

    while not open_set_start.empty() and not open_set_end.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        current_start_side = open_set_start.get()[2]
        current_end_side = open_set_end.get()[2]

        if current_start_side not in closed_set_start:
            if current_start_side in closed_set_end:
                return True, current_start_side

            for neighbor in [neighbor for neighbor in current_start_side.neighbors if neighbor is not None]:
                if neighbor not in closed_set_start:
                    temp_g_score = g_score_start[current_start_side] + 1
                    came_from_start[neighbor] = current_start_side
                    g_score_start[neighbor] = temp_g_score
                    f_score_start[neighbor] = temp_g_score + \
                        h(neighbor.get_pos(), end.get_pos())
                    count_start += 1
                    open_set_start.put(
                        (f_score_start[neighbor], count_start, neighbor))
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
                    temp_g_score = g_score_end[current_end_side] + 1
                    came_from_end[neighbor] = current_end_side
                    g_score_end[neighbor] = temp_g_score
                    f_score_end[neighbor] = temp_g_score + \
                        h(start.get_pos(), neighbor.get_pos())
                    count_end += 1
                    open_set_end.put(
                        (f_score_end[neighbor], count_end, neighbor))
                    if not neighbor.is_closed() and neighbor is not start and neighbor is not end:
                        neighbor.make_open_secondary()

            if current_end_side is not end and current_end_side is not start:
                current_end_side.make_closed_secondary()
            closed_set_end.append(current_end_side)

        draw()

    return False, None
