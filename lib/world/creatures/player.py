from lib.world.creatures._creature import Creature


class Player(Creature):
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
