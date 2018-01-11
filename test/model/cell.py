import  model.cell as cell


cells = [[0] * 10 for _ in range(10)]

for x in range(0, 10):
    for y in range(0, 10):
        cells[x][y] = cell.Cell(1, 1, 1, 1, 1)

print(len(cell.get_moore_neighborhood(cells, 0, 0)))
print(len(cell.get_moore_neighborhood(cells, 9, 0)))
print(len(cell.get_moore_neighborhood(cells, 0, 9)))
print(len(cell.get_moore_neighborhood(cells, 9, 9)))
print(len(cell.get_moore_neighborhood(cells, 5, 5)))
print(len(cell.get_moore_neighborhood(cells, 0, 5)))

