import numpy as np
from enum import Enum

cell_params = {
    'igni2burn': [1, 3],
    'ember2dead': [3, 5],
}


class CellState(Enum):
    """
    Selection the state for cell on the GRID
    """
    Soil = 0
    Ignited = 1
    Burning = 2
    Embers = 3
    DeadBurned = 4
    DefTree = 5


class TreeSize(Enum):
    tiny = 1
    normal = 2
    big = 3


class TreeType(Enum):
    """
    The options for tree type
    """
    Deciduous = 0
    Conifer = 1
    Hardwood = 2
    DryTree = 3


class Cell:
    def __init__(self, coordinates, state, altitude=0, size=TreeSize.normal, tree_type=TreeType.Deciduous):
        """
        :param coordinates:
        :param size: rough category for this tree
        :param state: selected state
        :param altitude: relative attitude
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.state = state
        self.altitude = altitude
        if self.state != CellState.Soil:
            self.size = size
            self.type = tree_type
            self.OUT_heat = self.out_heat_volume()
            self.embers_heat = self.OUT_heat * 0.07
            self.ember_time = np.random.randint(cell_params['ember2dead'][0],
                                                cell_params['ember2dead'][1])
        if self.state == CellState.DefTree:
            # Soil is just a soil, don't require to following attributes
            self.IN_heat = self.in_heat_volume()
            self.evo = np.random.randint(cell_params['igni2burn'][0],
                                         cell_params['igni2burn'][1])

    def can_burn(self):
        if self.state == CellState.DefTree:
            return True
        else:
            return False

    def in_heat_volume(self):
        res = 0
        if self.type == TreeType.DryTree:
            res = 10
        if self.type == TreeType.Conifer:
            res = 20
        if self.type == TreeType.Deciduous:
            res = 35
        if self.type == TreeType.Hardwood:
            res = 50
        return 8 * res * self.size.value

    def out_heat_volume(self):
        res = 0
        if self.type == TreeType.DryTree:
            res = 40
        if self.type == TreeType.Conifer:
            res = 45
        if self.type == TreeType.Deciduous:
            res = 40
        if self.type == TreeType.Hardwood:
            res = 30
        return 8 * res * self.size.value

    def burn_tree(self, around_heat=0):
        """
        Calculate the next state and other parameters for cell
        :param around_heat:
        :return: the heat volume from this cell
        """
        if self.state == CellState.DefTree:
            self.IN_heat -= around_heat
            if self.IN_heat <= 0:
                self.state = CellState.Ignited
                return True
            else:
                return False

    def step(self):
        """
        Calculate the next state and other parameters for cell
        :param around_heat:
        :return: the heat volume from this cell
        """
        # if self.state == CellState.DefTree:
        #     self.IN_heat -= around_heat
        #     if self.IN_heat <= 0:
        #         self.state = CellState.Ignited
        #         return self.OUT_heat * 0.3
        #     else:
        #         return 0
        if self.state == CellState.Ignited:
            self.evo -= 1
            if self.evo <= 0:
                self.state = CellState.Burning
                return self.OUT_heat
            else:
                return self.OUT_heat * 0.3
        if self.state == CellState.Burning:
            self.OUT_heat *= 0.9
            if self.OUT_heat <= 8:
                self.state = CellState.Embers
                return self.embers_heat
            else:
                return self.OUT_heat
        if self.state == CellState.Embers:
            self.ember_time -= 1
            if self.ember_time <= 0:
                self.state = CellState.DeadBurned
                return 0
            else:
                return self.embers_heat
        if self.state == CellState.Soil or self.state == CellState.DeadBurned:
            return 0

    def get_heat(self):
        """
        Calculate the next state and other parameters for cell
        :return: the heat volume from this cell
        """
        if self.state == CellState.DefTree:
            return 0
        if self.state == CellState.Ignited:
            return self.OUT_heat * 0.3
        if self.state == CellState.Burning:
            return self.OUT_heat
        if self.state == CellState.Embers:
            return self.embers_heat
        if self.state == CellState.Soil or self.state == CellState.DeadBurned:
            return 0

    def get_color(self):
        if self.state == CellState.DefTree:
            return 5 + self.type.value
        if self.state == CellState.Burning:
            if self.OUT_heat > 200:
                return 9
            elif self.OUT_heat < 100:
                return 11
            else:
                return 10
        else:
            return self.state.value
