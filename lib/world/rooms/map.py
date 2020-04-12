import random
import logging

logger = logging.getLogger(__name__)


class Area:
    def __init__(self, start_coords, end_coords):
        self.x_start, self.y_start = start_coords
        self.x_end, self.y_end = end_coords

    def get_random_coords(self) -> (int, int):
        return random.randint(self.x_start, self.x_end), random.randint(self.y_start, self.y_end)


class Tile:
    char = ' '
    blocked = False
    block_sight = False

    def __init__(self):
        self.is_visible = False
        self.seen = False


class Wall(Tile):
    char = '#'
    blocked = True
    block_sight = True



class Floor(Tile):
    char = '.'
    blocked = False
    block_sight = False



W = 'wall'
F = 'floor'
U = 'stairs_up'
D = 'stairs_down'
_ = None

TILE_MAP = {
    W: Wall,
    F: Floor,
}


class Map:
    def __init__(self):
        self._layers = []
        self._player_spawn_areas = None
        self._item_spawn_areas = None
        # todo: doors, connections to other rooms

        self.gen_random()
        self.map = self.make()

    def update_visible(self, x, y):
        '''
        needed for fov
        '''

        if y > len(self.map) - 1:
            return True
        if x > len(self.map[y]) - 1:
            return True

        self.map[y][x].is_visible = True
        self.map[y][x].seen = True

        return self.map[y][x].block_sight

    def gen_random(self):
        # todo: not so random right now

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

    def random_player_spawn(self):
        area: Area = random.choice(self._player_spawn_areas)
        return area.get_random_coords()

    def make(self):
        tmp = [_]
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

    def draw(self):
        result = []
        for row in self.map:
            result_row = [tile.char for tile in row]
            result.append(result_row)
        return result
