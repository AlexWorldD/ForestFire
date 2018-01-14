import model.cell as cell


class ForestModel:
    def __init__(self, rows, cols, tree_density):
        self.rows = rows
        self.cols = cols
        self.tree_density = tree_density
        self.init_state = cell.generate_initial_state(rows, cols, tree_density)

        self.current_state = self.init_state

    def run(self):
        return True

    def reset(self):
        return True

    def stop(self):
        return True

    def pause(self):
        return True

    def continue_run(self):
        return True
