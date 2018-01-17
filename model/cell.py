import random
from datetime import datetime
from enum import Enum

import numpy as np

import copy


class Cell:
    def __init__(self, state, heat, altitude):
        self.state = state
        self.heat = heat
        self.time = 0
        self.altitude = altitude

        self.type = None

    def set_virgin_type(self, type):
        self.type = type
        if self.type.value == 0:
            self.heat_treshold = 0.3
            self.heat_emission = 0.7
            self.burning_period = 4
        elif self.type.value == 1:
            self.heat_treshold = 0.2
            self.heat_emission = 0.6
            self.burning_period = 6

    def try_to_increase_burning_time(self):
        if self.time < self.burning_period:
            self.time += 1
            return True
        else:
            return False


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
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)):
        if not (0 <= x < len(cells_matrix) and 0 <= y < len(cells_matrix[x])):
            continue
        nb.append(cells_matrix[x][y])

    return nb


def get_moore_nb_matrix(cells_matrix, row, col):
    nb = np.array((3, 3), dtype=Cell)

    for x, y in ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)):
        if not (0 <= x < len(cells_matrix) and 0 <= y < len(cells_matrix[x])):
            nb[x][y] = None
        else:
            nb[x][y] = cells_matrix[x][y]

    return nb


def generate_initial_state(rows, cols, tree_density, conifer_density):
    cells = [[0] * rows for _ in range(cols)]
    for row in range(0, rows):
        for col in range(0, cols):
            cells[row][col] = Cell(CellState.Soil, 0.0, 1)

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


def apply_dumb_rule(cell, hood):
    new_cell = copy.deepcopy(cell)
    if cell.state.value == 0:
        ignited_cells = 0
        for nb in hood:
            if nb.state.value == 1 or nb.state.value == 2:
                ignited_cells += 1

        if ignited_cells > 1:
            new_cell.state = CellState.Ignited

    elif cell.state.value == 1:
        new_cell.state = CellState.Burning
    elif cell.state.value == 2:
        new_cell.state = CellState.ColdBurned
    return new_cell


def get_next_state(cells):
    rows = len(cells)
    cols = len(cells[0])
    result = [[0] * rows for _ in range(cols)]

    for row in range(0, rows):
        for col in range(0, cols):
            new_cell_state = apply_heat_with_wind_rule(cells[row][col], get_moore_nb_matrix(cells, row, col))
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


def increase_heat(cells_matrix, row, col):
    if cells_matrix[row][col].type is None:
        cells_matrix[row][col].set_virgin_type(VirginType.Hardwood)

    cells_matrix[row][col].state = CellState.Virgin
    cells_matrix[row][col].heat = 0.6

    return cells_matrix


def calculate_new_heat(cell, hood):
    heat_value = 0.0

    for nb in hood:
        if nb.state.value == 2:
            heat_value += nb.heat_emission
    heat_value = heat_value / 8.0 + cell.heat

    # print(heat_value)
    return heat_value


def apply_heat_rule(cell, hood):
    new_cell = copy.deepcopy(cell)
    if cell.state.value == 0:
        new_cell.heat = calculate_new_heat(cell, hood)
        if cell.heat > cell.heat_treshold:
            new_cell.state = CellState.Ignited
    elif cell.state.value == 1:
        new_cell.state = CellState.Burning
    elif cell.state.value == 2:
        print(cell.time)
        if new_cell.try_to_increase_burning_time() == False:
            new_cell.state = CellState.ColdBurned

    return new_cell


def get_wind_matrix(level):
    wind = [[1.1, 1.0, 1.0],
            [1.3, 1.0, 0.8],
            [1.1, 1.0, 1.0]]

    return wind


def calculate_new_heat_with_wind(cell, hood):
    heat_emission_hood = np.zeros((3, 3), dtype=np.float32)
    for row in hood:
        for col in row:
            if cell[row][col] is None or cell[row][col].state.value != 2:
                heat_emission_hood[row][col] = 0.0
            else:
                heat_emission_hood[row][col] = cell[row][col].heat_emission

    heat_value = np.sum(np.matmul(heat_emission_hood, get_wind_matrix(0))) / 8.0 + cell.heat
    # heat_value = heat_value / 8.0 + cell.heat

    # print(heat_value)
    return heat_value


def apply_heat_with_wind_rule(cell, hood):
    new_cell = copy.deepcopy(cell)
    if cell.state.value == 0:
        new_cell.heat = calculate_new_heat_with_wind(cell, hood)
        if cell.heat > cell.heat_treshold:
            new_cell.state = CellState.Ignited
    elif cell.state.value == 1:
        new_cell.state = CellState.Burning
    elif cell.state.value == 2:
        print(cell.time)
        if new_cell.try_to_increase_burning_time() == False:
            new_cell.state = CellState.ColdBurned

    return new_cell
