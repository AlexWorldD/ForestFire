import random as random
from enum import Enum


class Cell:
    def __init__(self, state, heat, T, altitude, type):
        self.state = state
        self.heat = heat
        self.T = T
        self.altitude = altitude
        self.type = type


class CellState(Enum):
    Virgin = 0
    Ignited = 1
    Burning = 2
    ColdBurned = 3
    Soil = 4


def get_moore_neighborhood(cells_matrix, row, col):
    nb = []

    for x, y in ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)):
        if not (0 <= x < len(cells_matrix) and 0 <= y < len(cells_matrix[x])):
            continue
        nb.append(cells_matrix[x][y])

    return nb


def generate_initial_state(rows, cols, tree_density):
    cells = [[0] * rows for _ in range(cols)]
    for row in range(0, rows):
        for col in range(0, cols):
            cells[row][col] = Cell(CellState.Soil, 1, 1, 1, 1)

    # fill n-first elements in array, then shuffle cells in each row and each rows in whole cell-matrix
    trees_amount = int(rows * cols * tree_density)
    current_amount = 0
    for row in range(0, rows):
        for col in range(0, cols):
            if current_amount < trees_amount:
                cells[row][col].state = CellState.Virgin
                current_amount += 1
    random.shuffle([random.shuffle(row) for row in cells])

    return cells


def ignite_tree(cells_matrix, row, col):
    (cells_matrix[row][col]).state = CellState.Ignited
    return cells_matrix
