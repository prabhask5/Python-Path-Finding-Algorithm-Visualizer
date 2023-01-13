import pygame
from PathFindingAlgorithms.AStar import astar
from PathFindingAlgorithms.BidirectionalAStar import bidirectional_astar
from PathFindingAlgorithms.BFS import bfs
from PathFindingAlgorithms.BidirectionalBFS import bidirectional_bfs
from PathFindingAlgorithms.DFS import dfs
from PathFindingAlgorithms.GeneticPathfinder import genetic
from PathFindingAlgorithms.GreedyBestFirst import greedy
from PathFindingAlgorithms.RandomWalk import random_walk
from MazeCreationAlgorithms.SimpleStairMaze import generate_simple_stair
from MazeCreationAlgorithms.BasicRandomMaze import generate_random_maze
from MazeCreationAlgorithms.RecursiveMaze import generate_recursive_maze


# intializing pygame metadata
pygame.init()
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Pathfinding Algorithm Visualizer")

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
MAHOGANY = (103, 10, 10)
TURQUOISE = (64, 224, 208)
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)
BACK = (255, 255, 204)


# Class implementation


class DropDown():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.original_main = main
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(
                    surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list, others_open):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(
            mpos) and all([not oo for oo in others_open])

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1


class Spot:
    def __init__(self, row, col, width, height, total_rows, total_cols, col_offset):
        self.row = row
        self.col = col
        self.true_col = self.col - col_offset
        self.x = col * width
        self.y = row * height
        self.color = WHITE
        self.last_color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.col_offset = col_offset

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_closed_secondary(self):
        return self.color == YELLOW

    def is_open_secondary(self):
        return self.color == PURPLE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def is_best(self):
        return self.color == RED

    def is_on_current_path(self):
        return self.color == RED

    def reset(self):
        self.color, self.last_color = WHITE, self.color

    def make_start(self):
        self.color, self.last_color = ORANGE, self.color

    def make_closed(self):
        self.color, self.last_color = RED, self.color

    def make_open(self):
        self.color, self.last_color = GREEN, self.color

    def make_closed_secondary(self):
        self.color, self.last_color = YELLOW, self.color

    def make_open_secondary(self):
        self.color, self.last_color = PURPLE, self.color

    def make_barrier(self):
        self.color, self.last_color = BLACK, self.color

    def make_end(self):
        self.color, self.last_color = BLUE, self.color

    def make_path(self):
        self.color, self.last_color = MAHOGANY, self.color

    def make_best(self):
        self.color, self.last_color = RED, self.color

    def make_genetic_player(self):
        self.color, self.last_color = TURQUOISE, self.color

    def make_on_current_path(self):
        self.color, self.last_color = RED, self.color

    def make_last_color(self):
        self.color, self.last_color = self.last_color, self.color

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        self.neighbors = [None for i in range(4)]  # 0 = U, 1 = D, 2 = L, 3 = R
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - self.col_offset].is_barrier():
            self.neighbors[1] = grid[self.row + 1][self.col - self.col_offset]

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col - self.col_offset].is_barrier():
            self.neighbors[0] = grid[self.row - 1][self.col - self.col_offset]

        # RIGHT
        if self.col - self.col_offset < self.total_cols - 1 and not grid[self.row][self.col - self.col_offset + 1].is_barrier():
            self.neighbors[3] = grid[self.row][self.col - self.col_offset + 1]

        # LEFT
        if self.col - self.col_offset > 0 and not grid[self.row][self.col - self.col_offset - 1].is_barrier():
            self.neighbors[2] = grid[self.row][self.col - self.col_offset - 1]

    def __lt__(self, other):
        return False

    def __str__(self):
        return f"True Row: {self.row}, True Col: {self.col - self.col_offset}, X: {self.x}, Y: {self.y}"


def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    words = text.split()

    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh


def make_grid(cols, rows, width, height):
    grid = []
    col_gap = (width - 200) // cols
    offset = 200 // col_gap
    row_gap = height // rows
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j + offset, col_gap, row_gap, rows, cols, offset)
            grid[i].append(spot)

    return grid


def draw_grid(win, cols, rows, width, height):
    col_gap = (width - 200) // cols
    offset = 200 // col_gap
    row_gap = height // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (200, i * row_gap),
                         (width, i * row_gap))
        for j in range(cols):
            pygame.draw.line(win, GREY, ((j + offset) * col_gap, 0),
                             ((j + offset) * col_gap, height))


backRect = pygame.Rect(0, 0, 200, HEIGHT)
playButton = pygame.Rect(20, 50, 160, 50)
basicFont = pygame.font.SysFont(None, 48)
legendFont = pygame.font.SysFont(None, 20)
helpFont = pygame.font.SysFont(None, 24)


def draw(win, grid, cols, rows, width, height):
    mouse_on_start = playButton.collidepoint(pygame.mouse.get_pos())
    start_button_colors = [GREEN, COLOR_ACTIVE]
    start_button_writing = ["RUN", "RUNNING"]
    screen.fill(WHITE)
    pygame.draw.rect(screen, BACK, backRect)
    pygame.draw.rect(
        screen, start_button_colors[mouse_on_start and not any(diff_generations_running)], playButton)
    text = basicFont.render(start_button_writing[any(diff_generations_running)], True, BLACK,
                            start_button_colors[mouse_on_start and not any(diff_generations_running)])
    textRect = text.get_rect()
    textRect.center = playButton.center
    screen.blit(text, textRect)
    for row in grid:
        for spot in row:
            spot.draw(screen)
    draw_grid(win, cols, rows, width, height)
    final_legend = legend
    last_y_pos = 350
    if not any(diff_generations_running):
        final_legend = {"Reset Grid": "R"}
        final_legend.update(legend.copy())
    for i in range(len(final_legend.keys())):
        key = list(final_legend.keys())[i]
        val = final_legend[key]
        y_pos = 350 + 25 * i
        last_y_pos = y_pos
        legend_element_rect = pygame.Rect(20, y_pos, 160, 15)
        pygame.draw.rect(screen, BACK, legend_element_rect)
        if type(val) is str:
            legend_element_text = legendFont.render(
                val + " - " + key, True, BLACK, BACK)
            legend_element_text_rect = legend_element_text.get_rect()
            legend_element_text_rect.center = legend_element_rect.center
            screen.blit(legend_element_text, legend_element_text_rect)
        else:
            legend_element_text = legendFont.render(
                " - " + key, True, BLACK, BACK)
            legend_element_text_rect = legend_element_text.get_rect()
            width_of_element = legend_element_text_rect.width + 20
            color_rect_x_pos = (200 - width_of_element) // 2
            legend_element_color_rect = pygame.Rect(
                color_rect_x_pos, y_pos, 20, 20)
            legend_element_text_rect.midleft = (
                color_rect_x_pos + 20, y_pos + 10)
            pygame.draw.rect(screen, val, legend_element_color_rect)
            screen.blit(legend_element_text, legend_element_text_rect)
    renderTextCenteredAt(help_text, helpFont, BLACK, 100,
                         last_y_pos + 50, screen, 160)
    mode_dd.draw(screen)
    path_dd.draw(screen)
    algo_dd.draw(screen)
    pygame.display.update()


def get_clicked_pos(pos, cols, rows, width, height):
    col_gap = (width - 200) // cols
    row_gap = height // rows
    offset = 200 // col_gap

    x, y = pos

    row = y // row_gap
    col = (x // col_gap) - offset

    return row, col


def reconstruct_path(came_from, current, draw):
    steps = 0
    while current in came_from:
        steps += 1
        current = came_from[current]
        if current is not start and current is not end:
            current.make_path()
        draw()
    return steps + 1


def reconstruct_path_bidirectional(came_from_start, came_from_end, current_start, current_end, start, end, draw):
    intersect_to_end_path = []
    while current_end in came_from_end:
        current_end = came_from_end[current_end]
        intersect_to_end_path.append(current_end)
    steps = len(intersect_to_end_path)
    intersect_to_end_path = intersect_to_end_path[::-1]
    for node in intersect_to_end_path:
        if node is not start and node is not end:
            node.make_path()
        draw()
    if current_start is not start and current_start is not end:
        current_start.make_path()
    draw()
    while current_start in came_from_start:
        steps += 1
        current_start = came_from_start[current_start]
        if current_start is not start and current_start is not end:
            current_start.make_path()
        draw()
    return steps + 1


algo_dd = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    20, 125, 160, 50,
    pygame.font.SysFont(None, 24),
    "Select Algorithm", ["A-Star", "Bidirectional A*", "Genetic Path", "Depth-first Search", "Breadth-first Search", "Bidirectional BFS", "Greedy Best-first", "Random Walk"])

path_dd = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    20, 200, 160, 50,
    pygame.font.SysFont(None, 24),
    "Select Maze Type", ["Recursive Division", "Basic Random", "Simple Stair"])

mode_dd = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    20, 275, 160, 50,
    pygame.font.SysFont(None, 24),
    "Select Mode", ["Select Start", "Select End", "Select Obstacle"])


ROWS = 80
COLUMNS = 100
grid = make_grid(COLUMNS, ROWS, WIDTH, HEIGHT)
run = True
algo_options = ["A-Star", "Bidirectional A*", "Genetic Path", "Depth-first Search",
                "Breadth-first Search", "Bidirectional BFS", "Greedy Best-first", "Random Walk"]
path_options = ["Recursive Division", "Basic Random", "Simple Stair"]
mode_options = ["Select Start", "Select End", "Select Obstacle"]
selected_algo = None
selected_path = None
selected_mode = None
start = None
end = None
diff_generations_running = [False for _ in range(9)]
# in order of: path, A*, B A*, Genetic, DFS, BFS, B BFS, Greedy, Random
legend = {"Quit Visualizer": "Esc",
          "Start": ORANGE, "End": BLUE, "Obstacle": BLACK}
help_text = "Welcome! Pick start and end nodes and draw obstacles using the ‘Select Mode’ tab. Generate more complex mazes using the ‘Select Maze Type’ tab. When start and end nodes are selected, choose an algorithm to find a path between them using the ‘’Select Algorithm’ tab."
diff_legend_states = [{"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot": RED, "Pending Spot": GREEN, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot From Start": RED, "Pending Spot From Start": GREEN, "Visited Spot From End": YELLOW, "Pending Spot From End": PURPLE, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Genetic Player": TURQUOISE, "Best Player": RED, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot": RED, "Pending Spot": GREEN, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot": RED, "Pending Spot": GREEN, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot From Start": RED, "Pending Spot From Start": GREEN, "Visited Spot From End": YELLOW, "Pending Spot From End": PURPLE, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Visited Spot": RED, "Pending Spot": GREEN, "Final Path": MAHOGANY},
                      {"Quit Visualizer": "Esc",
                       "Start": ORANGE, "End": BLUE, "Obstacle": BLACK, "Current Path": RED, "Final Path": MAHOGANY}]
# in order of: A*, B A*, Genetic, DFS, BFS, B BFS, Greedy, Random
diff_help_states = ["A* guarantees shortest path.", "Bidirectional A* guarantees shortest path.", "Genetic Path does not guarantee any found path.", "DFS does not guarantee shortest path.",
                    "BFS guarantees shortest path.", "Bidirectional BFS guarantees shortest path.", "Greedy Best-first does not guarantee shortest path.", "Random Walk does not guarantee any found path."]
while run:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0]:  # LEFT
            pos = pygame.mouse.get_pos()
            if backRect.collidepoint(pos):
                if playButton.collidepoint(pos) and selected_algo is not None and start is not None and end is not None:
                    for row in grid:
                        for spot in row:
                            if not (spot.is_start() or spot.is_end() or spot.is_barrier()):
                                spot.reset()
                            spot.update_neighbors(grid)
                    if selected_algo == "A-Star":
                        came_from = {}
                        diff_generations_running[0] = True
                        path_found = astar(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), grid, start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[0] = False
                    elif selected_algo == "Bidirectional A*":
                        came_from_start, came_from_end = {}, {}
                        diff_generations_running[1] = True
                        path_found, intersect_node = bidirectional_astar(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), grid, start, end, came_from_start, came_from_end)
                        if path_found:
                            path_length = reconstruct_path_bidirectional(came_from_start, came_from_end, intersect_node, intersect_node, start, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[1] = False
                    elif selected_algo == "Genetic Path":
                        came_from = {}
                        diff_generations_running[2] = True
                        path_found = genetic(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, start, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[2] = False
                    elif selected_algo == "Depth-first Search":
                        came_from = {}
                        diff_generations_running[3] = True
                        path_found = dfs(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[3] = False
                    elif selected_algo == "Breadth-first Search":
                        came_from = {}
                        diff_generations_running[4] = True
                        path_found = bfs(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[4] = False
                    elif selected_algo == "Bidirectional BFS":
                        came_from_start, came_from_end = {}, {}
                        diff_generations_running[5] = True
                        path_found, intersect_node = bidirectional_bfs(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from_start, came_from_end)
                        if path_found:
                            path_length = reconstruct_path_bidirectional(came_from_start, came_from_end, intersect_node, intersect_node, start, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[5] = False
                    elif selected_algo == "Greedy Best-first":
                        came_from = {}
                        diff_generations_running[6] = False
                        path_found = greedy(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[6] = False
                    elif selected_algo == "Random Walk":
                        came_from = {}
                        diff_generations_running[7] = True
                        path_found = random_walk(lambda: draw(
                            screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), start, end, came_from)
                        if path_found:
                            path_length = reconstruct_path(came_from, end, lambda: draw(
                                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT))
                            start.make_start()
                            end.make_end()
                            help_text = f"Path length: {path_length}"
                        else:
                            help_text = "Unfortunately, no path was found between the current start and end nodes."
                        diff_generations_running[7] = False
            else:
                row, col = get_clicked_pos(pos, COLUMNS, ROWS, WIDTH, HEIGHT)
                spot = grid[row][col]
                if selected_mode == "Select Obstacle":
                    if spot is not start and spot is not end:
                        spot.make_barrier()
                elif selected_mode == "Select Start":
                    if start is not None:
                        start.make_last_color()
                        if start.is_end():
                            if not end:
                                prev_spot = grid[start.row][start.true_col]
                                end = prev_spot
                            else:
                                start.reset()
                    if spot is end:
                        end = None
                    start = spot
                    spot.make_start()
                elif selected_mode == "Select End":
                    if end is not None:
                        end.make_last_color()
                        if end.is_start():
                            if not start:
                                prev_spot = grid[end.row][end.true_col]
                                start = prev_spot
                            else:
                                end.reset()
                    if spot is start:
                        start = None
                    end = spot
                    spot.make_end()
        elif pygame.mouse.get_pressed()[2]:  # RIGHT
            pos = pygame.mouse.get_pos()
            if not backRect.collidepoint(pos):
                row, col = get_clicked_pos(pos, COLUMNS, ROWS, WIDTH, HEIGHT)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                algo_dd.main = algo_dd.original_main
                path_dd.main = path_dd.original_main
                mode_dd.main = mode_dd.original_main
                selected_algo = None
                selected_path = None
                selected_mode = None
                start = None
                end = None
                grid = make_grid(COLUMNS, ROWS, WIDTH, HEIGHT)
                legend = {"Quit Visualizer": "Esc",
                          "Start": ORANGE, "End": BLUE, "Obstacle": BLACK}
                help_text = "Welcome! Pick start and end nodes and draw obstacles using the ‘Select Mode’ tab. Generate more complex mazes using the ‘Select Maze Type’ tab. When start and end nodes are selected, choose an algorithm to find a path between them using the ‘’Select Algorithm’ tab."
            if event.key == pygame.K_ESCAPE:
                run = False

    algo_others_open = []
    path_others_open = [algo_dd.draw_menu]
    mode_others_open = [algo_dd.draw_menu, path_dd.draw_menu]

    algo_selected_option = algo_dd.update(event_list, algo_others_open)
    if algo_selected_option >= 0:
        algo_dd.main = algo_dd.options[algo_selected_option]
        selected_algo = algo_options[algo_selected_option]
        legend = diff_legend_states[algo_selected_option]
        help_text = diff_help_states[algo_selected_option]

    path_selected_option = path_dd.update(event_list, path_others_open)
    if path_selected_option >= 0:
        path_dd.main = path_dd.options[path_selected_option]
        new_selected_path = path_options[path_selected_option]
        if new_selected_path == "Recursive Division" and not selected_path == "Recursive Division":
            diff_generations_running[8] = True
            generate_recursive_maze(lambda: draw(
                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), grid)
            diff_generations_running[8] = False
        elif new_selected_path == "Basic Random" and not selected_path == "Basic Random":
            diff_generations_running[8] = True
            generate_random_maze(grid)
            diff_generations_running[8] = False
        elif new_selected_path == "Simple Stair" and not selected_path == "Simple Stair":
            diff_generations_running[8] = True
            generate_simple_stair(lambda: draw(
                screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT), grid)
            diff_generations_running[8] = False
        selected_path = new_selected_path

    mode_selected_option = mode_dd.update(event_list, mode_others_open)
    if mode_selected_option >= 0:
        mode_dd.main = mode_dd.options[mode_selected_option]
        selected_mode = mode_options[mode_selected_option]

    draw(screen, grid, COLUMNS, ROWS, WIDTH, HEIGHT)

pygame.quit()
exit()
