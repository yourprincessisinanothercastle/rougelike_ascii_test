from lib.world._thing import Thing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lib.world.rooms._room import Room

class Creature(Thing):
    '''
    something that could move every tick
    '''
    def __init__(self):
        self.room: Room = None
        self.x = 0
        self.y = 0

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        raise NotImplementedError
    
 
