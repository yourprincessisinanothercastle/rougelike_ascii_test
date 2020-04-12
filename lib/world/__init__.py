from lib.world.rooms.room import Room
from typing import List

class World:
    def __init__(self):
        self.players = []
        self.rooms: List[Room] = []
        self.start_room: Room = None

        self.structure = None

        self.init_world()

    def init_world(self):
        self.start_room = Room()
        self.rooms.append(self.start_room)
        


    def add_player(self, player):
        self.players.append(player)