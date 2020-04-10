from lib.world.creatures._creature import Creature


class Player(Creature):
    def __init__(self):
        super().__init__()
        self.command_queue = []

    def add_command(self, command):
        self.command_queue.append(command)
        
    def get_next_command(self):
        if self.command_queue:
            return self.command_queue.pop(0)
        return None

    def move(self, dx, dy):
        target_tile = self.room.map.map[self.y + dy][self.x + dx]
        if not target_tile.blocked:
            self.x += dx
            self.y += dy
