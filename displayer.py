import time
import pygame
import math

DELAY_PARAMETER = 1

class Displayer:
    def __init__(self, maze):
        pygame.init()

        # set up screen
        self.size = (500, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Maze Solver")

        # set up cell width and height based on input maze
        self.maze = maze
        self.cell_width = self.size[0] / self.maze.ncols
        self.cell_height = self.size[1] / self.maze.nrows

        self.draw_maze()

    def draw_wall(self, origin, end):
        pygame.draw.line(self.screen, (0, 0, 0), \
                         origin, end, 2)

    # fill given cell
    def fill_cell(self, cell):
        #find center of the cell
        posx = int(math.floor((cell[0] + 0.5) * self.cell_width) + 1)
        posy = int(math.floor((cell[1] + 0.5) * self.cell_height) + 1)

        radius = int(math.floor(min(self.cell_width, self.cell_height) / 2.5) - 1)

        pygame.draw.circle(self.screen, (255, 0, 0), (posx, posy), radius)

    def draw_maze(self):
        # clear the screen
        self.screen.fill((255, 255, 255))

        # draw the blank maze
        for i in range(self.maze.nrows):
            for j in range(self.maze.ncols):
                cell = self.maze.get_cell_by_xy(i, j)   # get cell walls
                if cell[1] == 1:    # current cell has bottom wall
                    wall_origin = (i * self.cell_width \
                                   , j * self.cell_height + self.cell_height)
                    wall_end = (i * self.cell_width + self.cell_width \
                                , j * self.cell_height + self.cell_height)
                    self.draw_wall(wall_origin, wall_end)

                if cell[0] == 1:  # current cell has right wall
                    wall_origin = (i * self.cell_width + self.cell_width \
                                   , j * self.cell_height)
                    wall_end = (i * self.cell_width + self.cell_width \
                                , j * self.cell_height + self.cell_height)
                    self.draw_wall(wall_origin, wall_end)

        self.fill_cell(self.maze.start)
        self.fill_cell(self.maze.goal)

        # draw screen border
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.size[0], self.size[1]), 1)

        pygame.display.update()

    def draw_path(self, path):
        # redraw the blank maze
        self.draw_maze()

        for cell in path:
            self.fill_cell(cell)
            pygame.display.update()

            pygame.event.pump() # prevent windows crash? :|

            delay = DELAY_PARAMETER / (self.maze.nrows)
            time.sleep(delay)
