from queue import PriorityQueue
import pygame


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def greedy(draw, start, end, came_from, is_progressive_generation):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    closed_set = []

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

        current = open_set.get()[2]

        if current not in closed_set:
            if current is end:
                return True

            for neighbor in [neighbor for neighbor in current.neighbors if neighbor is not None]:
                if neighbor not in closed_set:
                    came_from[neighbor] = current
                    h_score = h(neighbor.get_pos(), end.get_pos())
                    count += 1
                    open_set.put((h_score, count, neighbor))
                    if neighbor is not start and neighbor is not end:
                        neighbor.make_open()

            if is_progressive_generation:
                draw()

            if current is not start and current is not end:
                current.make_closed()
            closed_set.append(current)

    return False
