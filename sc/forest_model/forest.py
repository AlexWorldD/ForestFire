from cell import *

forest_params = {
    'width': 50,
    'height': 50,
    'TreeDensity': 0.7,
    'TreeDistribution': {TreeType.Deciduous: 0.3, TreeType.Conifer: 0.4, TreeType.Hardwood: 0.2},
    'MAX_STEPS': 100,
    'InitFire': (0, 0),
    'FireSize': 2
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
        print('FireMe')

    def get_neighborhood(self, coordinates):
        nb = []
        neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        count = 0
        for shift in neighbour:
            n_row = coordinates[0] + shift[0]
            n_col = coordinates[1] + shift[1]
            if (n_row >= 0 and n_row < self.width) and (n_col >= 0 and n_col < self.height):
                nb.append((n_row, n_col))
        return nb
