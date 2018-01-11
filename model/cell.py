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
