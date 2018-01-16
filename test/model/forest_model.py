import model.forest_model as forest

f = forest.ForestModel(10, 10, 1.0, 50)

assert f.current_state == f.init_state


def print_cells_matrix(matrix):
    for row in range(0, len(matrix)):
        row_str = []
        for col in range(0, len(matrix[row])):
            row_str.append(matrix[row][col].state.value)
        print(row_str)


for _ in range(0, 11):
    print_cells_matrix(f.current_state)
    print("------------------")
    f.next()
