from cell import *
from pyics import *
import matplotlib
from matplotlib import colors

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

forest_params = {
    'width': 100,
    'height': 100,
    'TreeDensity': 1,
    'TreeDistribution': {TreeType.Deciduous: 0.3, TreeType.Conifer: 0.4, TreeType.Hardwood: 0.2},
    'MAX_STEPS': 400,
    'InitFire': (50, 50),
    'FireSize': (2, 2),
    # 0 - no wind, + left2right, - right2left
    'Wind': [2, 0],
    'AltitudeImpact': 1.2
}


class ForestModel(Model):
    def __init__(self):
        Model.__init__(self)
        self.make_param('treeDensity', forest_params['TreeDensity'])
        self.make_param('width', forest_params['width'])
        self.make_param('height', forest_params['height'])
        # self._param_width = forest_params['width']
        # self._param_height = forest_params['height']
        # self._param_treeDensity = forest_params['TreeDensity']
        self.treeDistribution = forest_params['TreeDistribution']
        self.make_param('MAX_STEPS', forest_params['MAX_STEPS'])
        self.make_param('InitFireX', forest_params['InitFire'][0])
        self.make_param('InitFireY', forest_params['InitFire'][1])
        self.make_param('WindX', forest_params['Wind'][0])
        self.make_param('WindY', forest_params['Wind'][1])
        # self.make_param('FireSize', forest_params['FireSize'])
        self.grid = np.zeros((self._param_width, self._param_height))
        self.T = 0
        self.TREES = dict()
        self.FIRE = dict()
        self.BORDER = dict()
        self.DEAD = []
        self.initial_grid()
        self.init_fire()
        self.update_grid()

    def initial_grid(self, random=True):
        # TODO add more options for varieties of trees positions
        if random:
            trees_location = [(it // self._param_width, it % self._param_height) for it in
                              np.random.choice(len(range(self._param_width * self._param_height)),
                                               size=(
                                                   round(
                                                       self._param_treeDensity * self._param_width * self._param_height)),
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
        point = (self._param_InitFireX, self._param_InitFireY)
        for x in range(f_size[0] + 1):
            for y in range(f_size[1] + 1):
                if (x >= 0 and x < self._param_width) and (y >= 0 and y < self._param_height):
                    fire.append((point[0] + x, point[1] + y))
        for it in fire:
            self.TREES[it] = Cell(it, state=CellState.Burning)
            self.FIRE[it] = self.TREES[it]

    def reset(self):
        """
                Restore basic state of our CA
        """
        self.grid = np.zeros((self._param_width, self._param_height))
        self.T = 0
        self.TREES = dict()
        self.FIRE = dict()
        self.BORDER = dict()
        self.DEAD = []
        self.initial_grid()
        self.init_fire()
        self.update_grid()

    def get_fire_border(self):
        self.BORDER = dict()
        for key, item in self.FIRE.items():
            neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
            for shift in neighbour:
                n_row = item.x + shift[0]
                n_col = item.y + shift[1]
                if (n_row >= 0 and n_row < self._param_width) and (n_col >= 0 and n_col < self._param_height) and (
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
            if (n_row >= 0 and n_row < self._param_width) and (n_col >= 0 and n_col < self._param_height) and (
                    (n_row, n_col) in self.TREES):
                nb.append((n_row, n_col))
        return nb

    def get_neighborhood_heat(self, coordinates):
        # 'Wind': [0.5, 0]
        HEAT = 0
        wind = (self._param_WindX, self._param_WindY)
        neighbour = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for shift in neighbour:
            n_row = coordinates[0] + shift[0]
            n_col = coordinates[1] + shift[1]
            if (n_row >= 0 and n_row < self._param_height) and (n_col >= 0 and n_col < self._param_width) and (
                    (n_row, n_col) in self.TREES):
                # Divide by 8 due to the 8 possible directions in out CA for every Cell
                _heat = self.TREES[(n_row, n_col)].get_heat() / 8
                if self.TREES[(n_row, n_col)].altitude < self.TREES[coordinates].altitude:
                    _heat *= forest_params['AltitudeImpact']
                if self.TREES[(n_row, n_col)].altitude > self.TREES[coordinates].altitude:
                    _heat /= forest_params['AltitudeImpact']
                # Wind mask
                _x = shift[1] * wind[0]
                _y = shift[0] * wind[1]
                if _x <0:
                    _heat *= (1 + abs(wind[0]))
                if _x >0:
                    _heat /= (1 + abs(wind[0]))
                if _y <0:
                    _heat *= (1 + abs(wind[1]))
                if _y >0:
                    _heat /= (1 + abs(wind[1]))
                HEAT += _heat
        return HEAT

    def step(self):
        self.T += 1
        if self.T >= self._param_MAX_STEPS:
            return True
        self.get_fire_border()
        patch_in = []
        patch_out = []
        for key, item in self.BORDER.items():
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
            self.grid[key[0]][key[1]] = item.get_color()
        for it in self.DEAD:
            self.grid[it[0]][it[1]] = 4

    def draw(self):
        """Draws the current state of the grid."""
        plt.cla()
        # if self._update_axis:
        #     self._update_axis = False
        #     _tmp = [0, self.width, self._axis_limits[3], self._axis_limits[3] + self.height]
        #     self._axis_limits = _tmp
        # plt.axis(self._axis_limits)
        # if not plt.gca().yaxis_inverted():
        #     plt.gca().invert_yaxis()
        # Soil = 0
        # Ignited = 1
        # Burning = 2
        # Embers = 3
        # DeadBurned = 4
        # DefTree = 5
        # Deciduous = 0
        # Conifer = 1
        # Hardwood = 2
        # DryTree = 3
        cmap = colors.ListedColormap(
            ['sienna', 'yellow', 'blue', 'maroon', 'black', 'palegreen', 'seagreen', 'darkgreen', 'tan',
             'red', 'orangered', 'salmon'])
        plt.imshow(self.grid, interpolation='none', cmap=cmap, vmax=11)
        plt.axis('image')
        # if self._update_axis:
        #     self._update_axis=False
        #     plt.set_ybound(100, 150)
        plt.title('t = %d' % self.T)
