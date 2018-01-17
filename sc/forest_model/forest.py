from cell import *

forest_params = {
    'width': 100,
    'height': 100,
    'TreeDensity': 1,
    'TreeDistribution': {TreeType.Deciduous: 0.3, TreeType.Conifer: 0.4, TreeType.Hardwood: 0.2},
    'MAX_STEPS': 100,
    'InitFire': (0, 0),
    'FireSize': 2,
    'Wind': [0.5, 0],
    'AltitudeImpact': 1.2
}


class ForestModel:
    def __init__(self):
        self.width = forest_params['width']
        self.height = forest_params['height']
        self.treeDensity = forest_params['TreeDensity']
        self.treeDistribution = forest_params['TreeDistribution']
        self.grid = np.zeros((self.width, self.height))
        self.T = 0
        self.TREES = dict()
        self.FIRE = dict()
        self.BORDER = dict()
        self.DEAD = []
        self.initial_grid()
        self.init_fire()

    def initial_grid(self, random=True):
        # TODO add more options for varieties of trees positions
        if random:
            trees_location = [(it // self.width, it % self.height) for it in
                              np.random.choice(len(range(self.width * self.height)),
                                               size=(round(self.treeDensity * self.width * self.height)),
                                               replace=False)]
        _st = 0
        _end = 0
        # TODO add clustering in future
        for key, item in self.treeDistribution.items():
            _end += round(item * len(trees_location))
            if _end <= len(trees_location):
                _cur_positions = trees_location[_st:_end]
                for it in _cur_positions:
                    self.TREES[it] = Cell(it, state=CellState.DefTree, tree_type=key)
                _st = _end
        #         If non-100%, just fill def trees
        if _st <= len(trees_location):
            for it in trees_location[_st:-1]:
                self.TREES[it] = Cell(it, state=CellState.DefTree, tree_type=TreeType.Deciduous)

    def init_fire(self):
        fire = []
        f_size = forest_params['FireSize']
        point = forest_params['InitFire']
        for x in range(f_size + 1):
            for y in range(f_size + 1):
                fire.append((point[0] + x, point[1] + y))
        for it in fire:
            self.TREES[it] = Cell(it, state=CellState.Burning)
            self.FIRE[it] = self.TREES[it]

    def get_fire_border(self):
        self.BORDER = dict()
        for key, item in self.FIRE.items():
            neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
            for shift in neighbour:
                n_row = item.x + shift[0]
                n_col = item.y + shift[1]
                if (n_row >= 0 and n_row < self.width) and (n_col >= 0 and n_col < self.height) and (
                        (n_row, n_col) in self.TREES) and self.TREES[
                    (n_row, n_col)].can_burn():
                    self.BORDER[(n_row, n_col)] = self.TREES[(n_row, n_col)]
        return self.BORDER

    def get_neighborhood(self, coordinates):
        # 0 0 0
        # 0 1 0
        # 0 0 0
        nb = []
        neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for shift in neighbour:
            n_row = coordinates[0] + shift[0]
            n_col = coordinates[1] + shift[1]
            if (n_row >= 0 and n_row < self.width) and (n_col >= 0 and n_col < self.height) and (
                    (n_row, n_col) in self.TREES):
                nb.append((n_row, n_col))
        return nb

    def get_neighborhood_heat(self, coordinates):
        # 'Wind': [0.5, 0]
        HEAT = 0
        wind = forest_params['Wind']
        neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for shift in neighbour:
            n_row = coordinates[0] + shift[0]
            n_col = coordinates[1] + shift[1]
            if (n_row >= 0 and n_row < self.width) and (n_col >= 0 and n_col < self.height) and (
                    (n_row, n_col) in self.TREES):
                # Divide by 8 due to the 8 possible directions in out CA for every Cell
                _heat = self.TREES[(n_row, n_col)].get_heat() / 8
                if self.TREES[(n_row, n_col)].altitude < self.TREES[coordinates].altitude:
                    _heat *= forest_params['AltitudeImpact']
                if self.TREES[(n_row, n_col)].altitude > self.TREES[coordinates].altitude:
                    _heat /= forest_params['AltitudeImpact']
                # Wind mask
                _x = shift[0] * wind[0]
                _y = shift[1] * wind[1]
                if _x == -1:
                    _heat *= (1 + abs(wind[0]))
                if _x == 1:
                    _heat /= (1 + abs(wind[0]))
                if _y == -1:
                    _heat *= (1 + abs(wind[1]))
                if _y == 1:
                    _heat /= (1 + abs(wind[1]))
                HEAT += _heat
        return HEAT

    def step(self):
        self.T += 1
        self.get_fire_border()
        patch_in = []
        patch_out = []
        for key, item in self.BORDER.items():
            # TODO add wind here!
            total_heat = self.get_neighborhood_heat(key)
            if item.burn_tree(total_heat):
                patch_in.append(key)
        for flame_key, flame_item in self.FIRE.items():
            if flame_item.step() == 0:
                # Tree has already burned
                patch_out.append(flame_key)
                # Update burned trees now
        for i in patch_out:
            del self.FIRE[i]
        for i in patch_in:
            self.FIRE[i] = self.BORDER[i]
        self.DEAD.extend(patch_out)
        # TODO we can call update_grid with settled interval, add to model_param
        self.update_grid()

    def update_grid(self):
        # TODO add patch techniques, not the full update
        # 0 already means soil
        for key, item in self.TREES.items():
            self.grid[key[0]][key[1]] = item.state.value
        for it in self.DEAD:
            self.grid[it[0]][it[1]] = 4
