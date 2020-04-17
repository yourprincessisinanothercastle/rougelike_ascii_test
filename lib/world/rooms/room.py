from lib.world.creatures._creature import Creature
from lib.world.creatures.player import Player
from lib.world.rooms.map import Map


class Room():
    def __init__(self):
        self.map: Map = None
        self.players = []
        self.creatures = []

        self.map = Map()

    def remove_player(self, player: Player):
        self.players.remove(player)
        player.room = None

    def remove_creature(self, creature: Creature):
        self.creatures.remove(creature)
        creature.room = None

    def spawn_player(self, player: Player):
        if player.room:
            player.room.remove_player(player)
        player.room = self
        self.players.append(player)
        x, y = self.map.get_player_spawn()
        player.set_coords(x, y)
    
    def spawn_creature(self, creature: Creature, x=None, y=None):
        if creature.room:
            creature.room.remove_creature(creature)
        creature.room = self
        self.creatures.append(creature)
        if not x and y:
            x, y = self.map.random_creature_spawn()
        creature.set_coords(x, y)
