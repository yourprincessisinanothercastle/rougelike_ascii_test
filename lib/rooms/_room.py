
class Room():
    def __init__(self):
        self.map = []

class Area:
    def __init__(self, start_coords, end_coords):
        self.x_start, self.y_start = start_coords
        self.x_end, self.y_end = end_coords

class Map:
    W = 'wall'
    F = 'floor'

    def __init__(self):
        self.layers = []
        self.player_spawn_areas = None
        self.item_spawn_areas = None
        # todo: doors, connections to other rooms

    def gen_random(self):
        # todo: not so random right now
        self.layers = [
            [
                [W,W,W,W,W,W,W,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,F,F,F,F,F,F,W],
                [W,W,W,W,W,W,W,W],
            ]
        ]

        self.player_spawn_areas = [
            Area((1,1), (2,2)) # upper left 
        ]
        self.item_spawn_areas = [
            Area((5,7),(6,8))  # bottom right
        ]

