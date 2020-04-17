import logging
from time import sleep

from asciimatics.event import KeyboardEvent
from asciimatics.screen import ManagedScreen

from lib.init_logging import init_logging
from lib.util.field_of_view import fov
from lib.world import World
from lib.world.creatures.player import Player

init_logging('debug')

logger = logging.getLogger(__name__)
logger.debug('test')

KEYS = dict(
    # action: key code
    up=ord('w'),
    down=ord('s'),
    left=ord('a'),
    right=ord('d'),
    fire=0xa,  # return
    quit=ord('q'),
)


class ScreenManager:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.world.start_room.spawn_player(self.player)
        self.screen = None

    def screen_print_with_player_offset(self, s, x, y, colour=7, attr=0, bg=0):
        centre_x = (self.screen.width // 2) - self.player.x
        centre_y = (self.screen.height // 2) - self.player.y
        self.screen.print_at(s, centre_x + x, centre_y + y, colour=colour, attr=attr, bg=bg)

    def handle_input(self, screen):
        event = self.screen.get_event()
        if event and type(event) == KeyboardEvent:
            if event.key_code == KEYS['quit']:
                return False
            if event.key_code == KEYS['up']:
                self.player.add_action(self.player.move, 0, -1)
            if event.key_code == KEYS['down']:
                self.player.add_action(self.player.move, 0, 1)
            if event.key_code == KEYS['left']:
                self.player.add_action(self.player.move, -1, 0)
            if event.key_code == KEYS['right']:
                self.player.add_action(self.player.move, 1, 0)
            if event.key_code == KEYS['fire']:
                self.player.shoot()
            
        return True

    def tick(self, dt):
        self.player.process_action_queue(dt)
        for creature in self.player.room.creatures:
            creature.process_action_queue(dt)

    def run(self):
        fps = 1 / 20
        with ManagedScreen() as screen:
            _continue = True
            self.screen = screen
            while _continue:
                # process the actions further!
                self.tick(fps)

                # handle input
                _continue = self.handle_input(screen)

                # clear screen buffer
                self.screen.clear_buffer(self.screen.COLOUR_WHITE, self.screen.A_NORMAL, self.screen.COLOUR_BLACK)

                # print command queue (idx 0 is the method, __name__ is the magic var for readable name)
                action_methods = ['%s %s,%s)' % (action[0].__name__, action[1][0], action[1][1]) for action in
                                  self.player.action_queue]
                self.screen.print_at('queue: %s' % ','.join(action_methods), 0, 1)
                self.screen.print_at('room: %s' % self.player.room, 0, 2)

                if self.player.fov_needs_update:
                    logger.debug('updating fov')
                    for idx_row, row in enumerate(self.player.room.map.tiles):
                        for idx_column, column in enumerate(self.player.room.map.tiles[idx_row]):
                            self.player.room.map.tiles[idx_row][idx_column].is_visible = False
                    fov(self.player.x, self.player.y, self.player.view_radius, self.player.room.map.update_visible)
                    self.player.fov_needs_update = False

                # render map, player is center
                for idx_row, row in enumerate(self.player.room.map.tiles):
                    for idx_column, column in enumerate(self.player.room.map.tiles[idx_row]):
                        tile_char = ' '
                        draw_colour = self.screen.COLOUR_WHITE
                        if self.player.room.map.tiles[idx_row][idx_column].is_visible:
                            tile_char = self.player.room.map.tiles[idx_row][idx_column].char
                            draw_colour = self.screen.COLOUR_WHITE
                        elif self.player.room.map.tiles[idx_row][idx_column].seen:
                            tile_char = self.player.room.map.tiles[idx_row][idx_column].char
                            draw_colour = self.screen.COLOUR_MAGENTA
                        self.screen_print_with_player_offset(tile_char, idx_column, idx_row, colour=draw_colour)

                self.player.draw(self, dt=fps)
                for creature in self.player.room.creatures:
                    if creature.current_tile.is_visible:
                        creature.draw(self, dt=fps)

                # draw the screen!
                self.screen.refresh()

                # wait a bit
                sleep(fps)



game = ScreenManager()
game.run()
