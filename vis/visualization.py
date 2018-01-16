"""
A simple example of an animated plot
"""
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

import model.forest_model as forest

'''
fig, ax = plt.subplots()

x = np.arange(0, 2 * np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


def animate(i):
    line.set_ydata(np.sin(x + i / 10.0))  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,


ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                              interval=25, blit=True)
plt.show()


'''


def convert_states_to_colors(matrix):
    #state_by_color = {0: 10, 1: 20, 2: 30, 3: 40, 4: 50}
    rows = len(matrix)
    cols = len(matrix[0])
    result = np.zeros((rows, cols), dtype=int)
    for i in range(0, rows):
        for j in range(0, cols):
            result[i][j] = matrix[i][j].state.value
    #print(result)

    return result


def run_model(steps, time_interval):
    f = forest.ForestModel(10, 10, 1.0, steps)
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


run_model(100, 1000)
