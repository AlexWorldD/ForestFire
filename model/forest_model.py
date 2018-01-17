import model.cell as cell


class ForestModel:
    def __init__(self, rows, cols, tree_density, steps, conifer_density):
        self.rows = rows
        self.cols = cols
        self.tree_density = tree_density
        self.conifer_density = conifer_density
        self.init_state = cell.generate_initial_state(rows, cols, tree_density, conifer_density)

        self.steps = steps
        self.current_state = self.init_state
        self.current_step = 0
        # TODO: add start_fire() func ?
        self.current_state = cell.increase_heat(self.current_state, 15, 15)
        self.current_state = cell.increase_heat(self.current_state, 16, 15)
        self.current_state = cell.increase_heat(self.current_state, 15, 14)
        self.current_state = cell.increase_heat(self.current_state, 16, 14)
    # TODO: run, stop, pause - continue : run model in coroutine, which returns next state with T(period)?
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
