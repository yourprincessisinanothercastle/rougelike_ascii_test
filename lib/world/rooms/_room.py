from lib.world.creatures.player import Player
import random


class Room():
    def __init__(self):
        self.map: Map = None
        self.players = []
        self.creatures = []

        self.map = Map()
        self.map.gen_random()

    def remove_player(self, player: Player):
        self.players.remove(player)
        player.room = None

    def spawn_player(self, player: Player):
        if player.room:
            player.room.remove_player(player)
        player.room = self
        self.players.append(player)
        x, y = self.map.random_player_spawn()
        player.set_coords(x, y)


class Area:
    def __init__(self, start_coords, end_coords):
        self.x_start, self.y_start = start_coords
        self.x_end, self.y_end = end_coords

    def get_random_coords(self) -> (int, int):
        return random.randint(self.x_start, self.x_end), random.randint(self.y_start, self.y_end)


W = 'wall'
F = 'floor'
_ = None


class Tile:
    SYMBOLS = dict(
        wall=dict(
            char='#',
            blocked=True,
            block_sight=True
        ),
        floor=dict(
            char='.',
            blocked=False,
            block_sight=False
        ),
    )
    DEFAULT_SYMBOL = dict(
        char=' ',
        blocked=False,
        block_sight=False
    ),

    def __init__(self, symbol):
        symbol = Tile.SYMBOLS.get(symbol, Tile.DEFAULT_SYMBOL)
        self.char = symbol['char']
        self.blocked = symbol['blocked']
        self.block_sight = symbol['block_sight']


class Map:
    def __init__(self):
        self._layers = []
        self._player_spawn_areas = None
        self._item_spawn_areas = None
        # todo: doors, connections to other rooms

        self.gen_random()
        self.map = self.make()

    def gen_random(self):
        # todo: not so random right now
        self._layers = [
            [
                [F, W, W, W, W, W, W, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [W, F, F, F, F, F, F, W],
                [F, W, W, W, W, F, W, F],
            ],
            [
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, W, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],

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
                        tile_at_index = Tile(element_at_index)
                        result[row_idx][col_idx] = tile_at_index
        return result

    def draw(self):
        result = []
        for row in self.map:
            result_row = [tile.char for tile in row]
            result.append(result_row)
        return result
        