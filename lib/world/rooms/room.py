from lib.world.creatures.player import Player
from lib.world.rooms.map import Map


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

