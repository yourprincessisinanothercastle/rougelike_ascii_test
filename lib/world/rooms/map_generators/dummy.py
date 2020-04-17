import random

from lib.world.rooms.map_generators import _MapGenerator, Area
from lib.world.rooms.tiles import Wall, Floor

W = 'wall'
F = 'floor'
_ = None

TILE_MAP = {
    W: Wall,
    F: Floor,
}


class DummyGenerator(_MapGenerator):
    def __init__(self):
        super().__init__()
        self.gen_random()
        self.map = self.make()

    def gen_random(self):
        self._layers = [
            [
                [F, W, W, W, W, W, W, W, F, W, W, W, W, W, W, W, F, W, W, W, W, W, W, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W, W, F, F, F, F, F, F, W],
                [F, W, W, W, W, F, W, F, F, W, W, W, W, F, W, F, F, W, W, W, W, F, W, F],
            ],
            [
                [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, W, _, _, _, _, _, _, _, W, _, _, _, _, _, _, _, W, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, W, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            ],
        ]

        self._player_spawn_areas = [
            Area((1, 1), (2, 2))  # upper left
        ]
        self._item_spawn_areas = [
            Area((5, 7), (6, 8))  # bottom right
        ]
        self._monster_spawn_areas = [
            Area((5, 7), (6, 8))  # bottom right
        ]

    def make(self):
        
        tmp = [' ']
        # inflate result map with Nones
        first_layer = self._layers[0]
        tmp = tmp * len(first_layer[0])  # a row with the length of the first row of the first layer
        result = []
        for x in range(len(first_layer)):
            result.append(tmp.copy())

        for layer in self._layers:
            for row_idx, row in enumerate(layer):
                for col_idx, char in enumerate(row):
                    element_at_index = layer[row_idx][col_idx]
                    if element_at_index:
                        tile_at_index = TILE_MAP[element_at_index]
                        result[row_idx][col_idx] = tile_at_index()
        return result
