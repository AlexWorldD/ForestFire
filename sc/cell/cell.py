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
    DefTree = 0
    Ignited = 1
    Burning = 2
    Embers = 3
    DeadBurned = 4
    Soil = 5


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
        if self.state == CellState.DefTree:
            # Soil is just a soil, don't require to following attributes
            self.size = size
            self.type = tree_type
            self.IN_heat = self.in_heat_volume()
            self.OUT_heat = self.out_heat_volume()
            self.evo = np.random.randint(cell_params['igni2burn'][0],
                                         cell_params['igni2burn'][1])
            self.embers_heat = self.OUT_heat * 0.07
            self.ember_time = np.random.randint(cell_params['ember2dead'][0],
                                                cell_params['ember2dead'][1])

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

    def step(self, around_heat):
        """
        Calculate the next state and other parameters for cell
        :param around_heat:
        :return:
        """
        if self.state == CellState.DefTree:
            self.IN_heat -= around_heat
            if self.IN_heat <= 0:
                self.state = CellState.Ignited
        if self.state == CellState.Ignited:
            self.evo -= 1
            if self.evo <= 0:
                self.state = CellState.Burning
        if self.state == CellState.Burning:
            self.OUT_heat *= 0.9
            if self.OUT_heat <= 8:
                self.state = CellState.Embers
        if self.state == CellState.Embers:
            self.ember_time -= 1
            if self.ember_time <= 0:
                self.state = CellState.DeadBurned
