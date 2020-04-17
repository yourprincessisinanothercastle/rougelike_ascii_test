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