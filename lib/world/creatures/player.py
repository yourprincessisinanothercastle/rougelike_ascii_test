from lib.world.creatures._creature import Creature
import logging

logger = logging.getLogger(__name__)

class Player(Creature):
    DIRECTIONS = dict(
        up='up',
        down='down',
        left='left',
        right='right',
    )

    CHARS = dict(
        up='◓',
        down='◒',
        left='◐',
        right='◑',
    )

    def __init__(self):
        super().__init__()
        self.command_queue = []
        self.direction = Player.DIRECTIONS['left']

    @property
    def char(self):
        return Player.CHARS[self.direction]

    def add_command(self, command):
        self.command_queue.append(command)

    def get_next_command(self):
        if self.command_queue:
            return self.command_queue.pop(0)
        return None

    def move(self, dx, dy):
        target_tile = self.room.map.map[self.y + dy][self.x + dx]
        if dx > 0:
            new_direction = Player.DIRECTIONS['right']
        elif dx < 0:
            new_direction = Player.DIRECTIONS['left']
        elif dy > 0:
            new_direction = Player.DIRECTIONS['down']
        else:
            new_direction = Player.DIRECTIONS['up']

        if self.direction != new_direction:
            self.direction = new_direction
            return
                
        if not target_tile.blocked:
            self.x += dx
            self.y += dy
