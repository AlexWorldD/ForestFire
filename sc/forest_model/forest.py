from cell import *

forest_params = {
    'width': 5,
    'height': 5,
    'TreeDensity': 0.7,
    'TreeDistribution': {TreeType.Deciduous: 0.3, TreeType.Conifer: 0.4, TreeType.Hardwood: 0.2}
}


class ForestModel:
    def __init__(self):
        self.width = forest_params['width']
        self.height = forest_params['height']
        self.treeDensity = forest_params['TreeDensity']
        self.treeDistribution = forest_params['TreeDistribution']
        self.grid = np.zeros((self.width, self.height))
        self.TREES = dict()
        self.FIRE = dict()
        self.initial_grid()

    def initial_grid(self, random=True):
        # TODO add more options for varieties of trees positions
        if random:
            trees_location = [(it // self.width, it % self.height) for it in
                              np.random.choice(len(range(self.width * self.height)),
                                               size=(round(self.treeDensity * self.width * self.height)),
                                               replace=False)]
        _st = 0
        _end = 0
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
