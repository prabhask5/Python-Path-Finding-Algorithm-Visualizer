import pygame
import random


def generate_recursive_maze(draw, grid):
    for row in grid:
        for spot in row:
            spot.reset()

    generate_surrouding_walls(draw, grid)
    recursive_division_maze(draw, grid, 2, len(
        grid) - 3, 2, len(grid[0]) - 3, "horizontal")


def recursive_division_maze(draw, grid, row_start, row_end, col_start, col_end, orientation):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()

    if row_end < row_start or col_end < col_start:
        return

    if orientation == "horizontal":
        current_row = random.choice(range(row_start, row_end + 1, 2))
        skip_col = random.choice(range(col_start - 1, col_end + 2, 2))
        for spot in grid[current_row][col_start - 1: col_end + 2]:
            if spot.true_col != skip_col:
                spot.make_barrier()
                draw()
        if current_row - 2 - row_start > col_end - col_start:
            recursive_division_maze(
                draw, grid, row_start, current_row - 2, col_start, col_end, orientation)
        else:
            recursive_division_maze(
                draw, grid, row_start, current_row - 2, col_start, col_end, "vertical")
        if row_end - (current_row + 2) > col_end - col_start:
            recursive_division_maze(
                draw, grid, current_row + 2, row_end, col_start, col_end, orientation)
        else:
            recursive_division_maze(
                draw, grid, current_row + 2, row_end, col_start, col_end, "vertical")
    elif orientation == "vertical":
        current_col = random.choice(range(col_start, col_end + 1, 2))
        skip_row = random.choice(range(row_start - 1, row_end + 2, 2))
        for spot in [row[current_col] for row in grid[row_start - 1: row_end + 2]]:
            if spot.row != skip_row:
                spot.make_barrier()
                draw()
        if row_end - row_start > current_col - 2 - col_start:
            recursive_division_maze(
                draw, grid, row_start, row_end, col_start, current_col - 2, "horizontal")
        else:
            recursive_division_maze(
                draw, grid, row_start, row_end, col_start, current_col - 2, orientation)
        if row_end - row_start > col_end - (current_col + 2):
            recursive_division_maze(
                draw, grid, row_start, row_end, current_col + 2, col_end, "horizontal")
        else:
            recursive_division_maze(
                draw, grid, row_start, row_end, current_col + 2, col_end, orientation)


def generate_surrouding_walls(draw, grid):
    closed_set = []

    for i in range(len(grid[0])):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
        current_up = grid[0][i]
        current_down = grid[len(grid) - 1][i]
        if current_up not in closed_set:
            current_up.make_barrier()
            closed_set.append(current_up)
        if current_down not in closed_set:
            current_down.make_barrier()
            closed_set.append(current_down)
        draw()

    for i in range(len(grid)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
        current_left = grid[i][0]
        current_right = grid[i][len(grid[0]) - 1]
        if current_left not in closed_set:
            current_left.make_barrier()
            closed_set.append(current_left)
        if current_right not in closed_set:
            current_right.make_barrier()
            closed_set.append(current_right)
        draw()
