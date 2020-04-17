import random


class Area:
    def __init__(self, start_coords, end_coords):
        self.x_start, self.y_start = start_coords
        self.x_end, self.y_end = end_coords

    def get_random_coords(self) -> (int, int):
        return random.randint(self.x_start, self.x_end), random.randint(self.y_start, self.y_end)


class _MapGenerator:
    def __init__(self):
        self.map = None
        self._player_spawn_areas = []
        self._item_spawn_areas = []
        self._monster_spawn_areas = []

    def make(self):
        raise NotImplementedError
