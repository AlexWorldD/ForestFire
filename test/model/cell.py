import random as random

import model.cell as cell
from model.cell import Cell
from model.cell import CellState

cells = [[0] * 10 for _ in range(10)]

for x in range(0, 10):
    for y in range(0, 10):
        cells[x][y] = Cell(cell.CellState(random.randint(0, 4)), 1, 1, 1, 1)

print(len(cell.get_moore_neighborhood(cells, 0, 0)))
print(len(cell.get_moore_neighborhood(cells, 9, 0)))
print(len(cell.get_moore_neighborhood(cells, 0, 9)))
print(len(cell.get_moore_neighborhood(cells, 9, 9)))
print(len(cell.get_moore_neighborhood(cells, 5, 5)))
print(len(cell.get_moore_neighborhood(cells, 0, 5)))

cells = cell.generate_initial_state(10, 10, 0.3)

trees = 0
for x in range(0, 10):
    for y in range(0, 10):
        if (cells[x][y]).state == CellState.Virgin:
            trees += 1

assert trees == int(10 * 10 * 0.3)

cells = cell.ignite_tree(cells, 3, 4)

assert cells[3][4].state == CellState.Ignited


def print_cells_matrix(matrix):
    for row in range(0, len(matrix)):
        row_str = []
        for col in range(0, len(matrix[row])):
            row_str.append(matrix[row][col].state.value)
        print(row_str)


cells = cell.generate_initial_state(5, 5, 0.1)
print_cells_matrix(cells)
print("---------------")
new_cells = cell.get_next_state(cells)
print_cells_matrix(new_cells)


