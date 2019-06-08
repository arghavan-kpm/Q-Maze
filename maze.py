from __future__ import absolute_import
from __future__ import print_function
import time
import sys

from displayer import *
from solver import *
from random import choice
from six.moves import range
from six.moves import input

ADJACENT_DELTA = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def validate_answer(maze, path):
    if maze.start not in path:
        raise AssertionError('Start Not in Path')

    if maze.goal not in path:
        raise AssertionError('Goal Not in Path')

    path_set = set(path)
    for cell in path:
        neighbor_set = set(maze.get_neighbors(cell))
        if len(neighbor_set.intersection(path_set)) == 0:
            raise AssertionError('Disjoint cell found!')


class Maze:
    def __init__(self):
        self.cells = []  # 2d array of characters. for each cell store if it has RIGHT or BOTTOM wall
        self.nrows = None
        self.ncols = None
        self.start = ()  # starting cell
        self.goal = ()  # target cell

    # return maze as text
    def __str__(self):
        ret_val = ""

        for i in range(self.nrows):
            for j in range(self.ncols):
                cell_value = 0
                if self.get_cell_by_xy(j, i)[0] == 1:
                    cell_value += 1;
                if self.get_cell_by_xy(j, i)[1] == 1:
                    cell_value += 2;

                ret_val += str(cell_value)

            ret_val += "\n"

        return ret_val

    def setup_maze(self):
        print(" 1) load maze")
        print(" 2) generate random maze")
        print(" 3) exit")
        command = input()

        if "1" in command:
            print("maze file name?")
            file_name = input()

            try:
                self.read_from_file(file_name)
                return
            except IOError as e:
                print("could not read file. generate random 20x20 maze..")
                self.generate_maze(20, 20)
                return

        if "2" in command:
            print("Maze size? [Recom.: 10, 25, 50, 100] [Max: 100]")
            maze_size = int(input())
            self.generate_maze(maze_size, maze_size)
            return

        if "3" in command:
            sys.exit()

    def get_cell_by_xy(self, x, y):
        return self.cells[x][y]

    def get_cell(self, cell):
        return self.cells[cell[0]][cell[1]]

    # check if wall exists between two cells
    def check_wall(self, cell, ncell):
        #  print cell, self.get_cell(cell), ncell, self.get_cell(ncell)
        if cell[0] - ncell[0] == 1:  # cell is right of ncell
            return self.get_cell(ncell)[0]
        elif cell[0] - ncell[0] == -1:  # cell is left of ncell
            return self.get_cell(cell)[0]
        elif cell[1] - ncell[1] == 1:  # cell is under ncell
            return self.get_cell(ncell)[1]
        elif cell[1] - ncell[1] == -1:  # cell is top of ncell
            return self.get_cell(cell)[1]
        else:  # cell and ncell are not adjacent
            return 1

    # get neighbors of a given cell
    def get_neighbors(self, cell):
        around = [(cell[0] + dx, cell[1] + dy) for dx, dy in ADJACENT_DELTA]
        return [x for x in around if self.cell_is_valid(x) and self.check_wall(cell, x) == 0]

    # read maze from file funcitons
    def read_from_file(self, filename):

        maze_file = open(filename).readlines()

        self.init_blank_maze(len(maze_file), len(maze_file[0].strip('\n')))

        self.start = (0, self.nrows - 1)
        self.goal = (self.ncols - 1, 0)

        for j in range(len(maze_file)):
            row = maze_file[j].strip('\n')
            for i in range(len(row)):
                if "0" in row[i]:
                    self.get_cell_by_xy(i, j)[0] = 0
                    self.get_cell_by_xy(i, j)[1] = 0
                elif "1" in row[i]:
                    self.get_cell_by_xy(i, j)[0] = 1
                    self.get_cell_by_xy(i, j)[1] = 0
                elif "2" in row[i]:
                    self.get_cell_by_xy(i, j)[0] = 0
                    self.get_cell_by_xy(i, j)[1] = 1
                elif "3" in row[i]:
                    self.get_cell_by_xy(i, j)[0] = 1
                    self.get_cell_by_xy(i, j)[1] = 1
                else:
                    raise IOError("invalid input")

    # maze generation functions
    # initialize maze with all walls
    def init_blank_maze(self, width, height):
        self.nrows = height
        self.ncols = width

        for row in range(self.nrows):
            self.cells.append([])
            for col in range(self.ncols):
                self.cells[row].append([1, 1])  # first element is for right wall, second for south

    def remove_wall(self, cell1, cell2):
        if cell1[1] - cell2[1] == 1:  # cell2 is top of cell1
            self.get_cell(cell2)[1] = 0
        elif cell1[1] - cell2[1] == -1:  # cell1 is top of cell2
            self.get_cell(cell1)[1] = 0
        elif cell1[0] - cell2[0] == 1:  # cell2 is left of cell1
            self.get_cell(cell2)[0] = 0
        elif cell1[0] - cell2[0] == -1:  # cell1 is left of cell2
            self.get_cell(cell1)[0] = 0

    # generate maze with recursive backtracker method
    def generate_maze(self, width, height):
        self.init_blank_maze(width, height)

        # bottom left corner is always start
        self.start = (0, self.nrows - 1)
        self.goal = (self.ncols - 1, 0)

        num_of_cells = self.nrows * self.ncols

        current_cell = self.start
        backtrack_stack = []

        visited_cells = [current_cell]  # initial visited cells list
        while len(visited_cells) < num_of_cells:
            # get neighbors that are not visited
            current_neighbors = [(current_cell[0] + dx, current_cell[1] + dy) for dx, dy in ADJACENT_DELTA]
            unvisited_neighbors = [x for x in current_neighbors if x not in visited_cells and self.cell_is_valid(x)]

            if len(unvisited_neighbors) > 0:
                neighbor = choice(unvisited_neighbors)
                backtrack_stack.append(current_cell)

                self.remove_wall(current_cell, neighbor)

                # choose one of the neighbors randomly
                current_cell = neighbor
                visited_cells.append(current_cell)

            elif len(backtrack_stack) > 0:
                current_cell = backtrack_stack.pop()

    def cell_is_valid(self, cell):
        if ((cell[0] < 0 or cell[0] >= self.nrows) \
                or (cell[1] < 0 or cell[1] >= self.ncols)):
            return False

        return True


if __name__ == "__main__":
    m = Maze()
    m.setup_maze()
    d = Displayer(m)
    
    print(">> Testing Q learning solver...")
    bfs_path = solver(m)
    try:
        validate_answer(m, bfs_path)  # m.goal in bfs_path:
        print(("solved maze. cost: ", len(bfs_path), "cells visited"))
        print ("Display solution? [y/n]")
        display_command =input()
        if "y" in display_command:
            d.draw_path(bfs_path)
    except AssertionError as e:
        print(("answer is invalid: " + e.message))
    
    print(" 1) Save maze to file")
    print(" 2) exit")
    command = input()

    if "1" in command:
        file_name = input("Enter file name:  ")
        try:
            f = open(file_name, "w")
            f.write(str(m))
            f.close()
        except IOError as e:
            print("save to file failed.")
            sys.exit()

    if "2" in command:
        sys.exit()
