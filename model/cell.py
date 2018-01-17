import random
from datetime import datetime
from enum import Enum

import numpy as np


class Cell:
    def __init__(self, state, heat, T, altitude):
        self.state = state
        self.heat = heat
        self.T = T
        self.altitude = altitude

        self.type = None

    def set_virgin_type(self, type):
        self.type = type
        if self.type.value == 0:
            self.heat_treshold = 0.5
            self.heat_emission = 0.5
        elif self.type.value == 1:
            self.heat_treshold = 0.4
            self.heat_emission = 0.4


class CellState(Enum):
    Virgin = 0
    Ignited = 1
    Burning = 2
    ColdBurned = 3
    Soil = 4


class VirginType(Enum):
    Conifer = 0
    Hardwood = 1


def get_moore_neighborhood(cells_matrix, row, col):
    nb = []

    for x, y in ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)):
        if not (0 <= x < len(cells_matrix) and 0 <= y < len(cells_matrix[x])):
            continue
        nb.append(cells_matrix[x][y])

    return nb


def generate_initial_state(rows, cols, tree_density, conifer_density):
    cells = [[0] * rows for _ in range(cols)]
    for row in range(0, rows):
        for col in range(0, cols):
            cells[row][col] = Cell(CellState.Soil, 1, 1, 1)

    # fill n-first elements in array, then shuffle cells in each row and each rows in whole cell-matrix
    trees_amount = int(rows * cols * tree_density)
    conifer_amount = int(trees_amount * conifer_density)
    current_amount = 0

    for row in range(0, rows):
        for col in range(0, cols):
            if current_amount < trees_amount:
                cells[col][row].state = CellState.Virgin

                # obviously hardwood_amount <= trees_amount - conifer_amount
                if current_amount < conifer_amount:
                    cells[col][row].set_virgin_type(VirginType.Conifer)
                else:
                    cells[col][row].set_virgin_type(VirginType.Hardwood)

                current_amount += 1
    random.seed(datetime.now())

    random.shuffle(cells)
    for sublist in cells:
        random.shuffle(sublist)

    return cells


def apply_dump_rule(cell, hood):
    if cell.state.value == 0:
        ignited_cells = 0
        for nb in hood:
            if nb.state.value == 1 or nb.state.value == 2:
                ignited_cells += 1

        if ignited_cells > 1:
            cell.state = CellState.Ignited

    elif cell.state.value == 1:
        cell.state = CellState.Burning
    elif cell.state.value == 2:
        cell.state = CellState.ColdBurned
    return cell


def get_next_state(cells):
    rows = len(cells)
    cols = len(cells[0])
    result = [[0] * rows for _ in range(cols)]

    for row in range(0, rows):
        for col in range(0, cols):
            new_cell_state = apply_dump_rule(cells[row][col], get_moore_neighborhood(cells, row, col))
            result[row][col] = new_cell_state

    return result


def shuffle_matrix(matrix):
    m = np.asmatrix(matrix, dtype=Cell)
    np.random.shuffle(m)

    return m.tolist()


def ignite_tree(cells_matrix, row, col):
    # TODO: fix this
    if cells_matrix[row][col].type is None:
        cells_matrix[row][col].set_virgin_type(VirginType.Hardwood)

    (cells_matrix[row][col]).state = CellState.Ignited
    return cells_matrix
