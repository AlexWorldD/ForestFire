"""
A simple example of an animated plot
"""
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

import model.forest_model as forest


def convert_states_to_colors(matrix):
    # state_by_color = {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}
    rows = len(matrix)
    cols = len(matrix[0])
    result = np.zeros((rows, cols), dtype=int)
    for i in range(0, rows):
        for j in range(0, cols):
            result[i][j] = matrix[i][j].state.value
    # print(result)

    return result


def run_model(steps, time_interval):
    f = forest.ForestModel(10, 10, 1.0, steps, 0.6)
    colored_states = convert_states_to_colors(f.current_state)
    fig = plt.figure()
    cmap = colors.ListedColormap(['green', 'yellow', 'red', 'black', 'black'])

    bounds = [0, 1, 2, 3, 4, 5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plot = plt.imshow(colored_states, cmap=cmap, norm=norm)

    def init():
        colored_states = convert_states_to_colors(f.current_state)
        plot.set_data(colored_states)
        return [plot]

    def animate(step):
        colored_states = convert_states_to_colors(f.next())
        plot.set_data(colored_states)
        return [plot]

    ani = animation.FuncAnimation(fig, animate, frames=steps,
                                  init_func=init, interval=time_interval, blit=True)

    plt.show()


def convert_virgin_types_to_colors(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = np.zeros((rows, cols), dtype=int)
    for i in range(0, rows):
        for j in range(0, cols):
            if matrix[i][j].state.value < 4:
                if matrix[i][j].type.value == 0:
                    result[i][j] = 1
                else:
                    result[i][j] = 2
            else:
                result[i][j] = 0

    return result


def show_virgin_type_map(cells):
    colored_map = convert_virgin_types_to_colors(cells)

    plt.figure()
    cmap = colors.ListedColormap(['white', 'green', 'cyan'])
    bounds = [0, 1, 2, 3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.title("Virgin types map")
    plt.imshow(colored_map, cmap=cmap, norm=norm)
    plt.show()
