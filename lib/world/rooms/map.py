import random
import logging

from lib.world.rooms.map_generators import Area
from lib.world.rooms.map_generators.dummy import DummyGenerator

logger = logging.getLogger(__name__)



class Map:
    def __init__(self, generator=DummyGenerator):
        self._layers = []
        # todo: doors, connections to other rooms

        self.map = DummyGenerator()
        self.tiles = self.map.map

    def update_visible(self, x, y):
        '''
        needed for fov
        '''

        if y > len(self.tiles) - 1:
            return True
        if x > len(self.tiles[y]) - 1:
            return True

        self.tiles[y][x].is_visible = True
        self.tiles[y][x].seen = True

        return self.tiles[y][x].block_sight

    def get_player_spawn(self):
        area: Area = random.choice(self.map._player_spawn_areas)
        return area.get_random_coords()

    def draw(self):
        result = []
        for row in self.tiles:
            result_row = [tile.char for tile in row]
            result.append(result_row)
        return result
