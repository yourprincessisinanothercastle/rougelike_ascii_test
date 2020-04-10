from asciimatics.screen import ManagedScreen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText, StaticRenderer
from time import sleep

from lib.world import World
from lib.world.creatures.player import Player

UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
QUIT = 'q'

class ScreenManager:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.world.start_room.spawn_player(self.player)

    def screen_print(self, screen, s, x, y):
        centre_x = (screen.width // 2) - self.player.x
        centre_y = (screen.height // 2) - self.player.y
        screen.print_at(s, centre_x + x, centre_y + y)

    def handle_input(self, screen):
        event = screen.get_event()
        if event:
            if event.key_code == ord(QUIT):
                return False
            if event.key_code == ord(UP):
                self.player.move(0, -1)
            if event.key_code == ord(DOWN):
                self.player.move(0, 1)
            if event.key_code == ord(LEFT):
                self.player.move(-1, 0)
            if event.key_code == ord(RIGHT):
                self.player.move(1, 0)
        return True

    def run(self):
        with ManagedScreen() as screen:
            _continue = True
            while _continue:
                screen.clear_buffer(screen.COLOUR_WHITE, screen.A_NORMAL, screen.COLOUR_BLACK)
                for idx, line in enumerate(self.player.room.map.draw()):
                    self.screen_print(screen, line, 0, idx)
                self.screen_print(screen, '@', self.player.x, self.player.y)
                screen.refresh()
                sleep(1/20)
                _continue = self.handle_input(screen)


game = ScreenManager()
game.run()

