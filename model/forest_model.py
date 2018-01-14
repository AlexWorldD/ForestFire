import model.cell as cell


class ForestModel:
    def __init__(self, rows, cols, tree_density, steps):
        self.rows = rows
        self.cols = cols
        self.tree_density = tree_density
        self.init_state = cell.generate_initial_state(rows, cols, tree_density)

        self.steps = steps
        self.current_state = self.init_state
        self.current_step = 0

        self.current_state = cell.ignite_tree(self.current_state, 2, 2)
        self.current_state = cell.ignite_tree(self.current_state, 2, 3)

    def run(self):
        return True

    def reset(self):
        self.current_state = self.init_state
        self.current_step = 0

    def next(self):
        if self.current_step < self.steps:
            self.current_state = cell.get_next_state(self.current_state)
            self.current_step += 1

        return self.current_state

    def stop(self):
        return True

    def pause(self):
        return True

    def continue_run(self):
        return True
