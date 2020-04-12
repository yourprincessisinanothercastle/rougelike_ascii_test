from asciimatics.screen import ManagedScreen
from time import sleep

from lib.util.field_of_view import fov
from lib.world import World
from lib.world.creatures.player import Player

import logging
from lib.init_logging import init_logging

init_logging('debug')

logger = logging.getLogger(__name__)
logger.debug('test')

KEYS = dict(
    # action: key code
    up=ord('w'),
    down=ord('s'),
    left=ord('a'),
    right=ord('d'),
    quit=ord('q'),
)


class ScreenManager:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.world.start_room.spawn_player(self.player)

    def screen_print_with_player_offset(self, screen, s, x, y,  colour=7, attr=0, bg=0):
        centre_x = (screen.width // 2) - self.player.x
        centre_y = (screen.height // 2) - self.player.y
        screen.print_at(s, centre_x + x, centre_y + y, colour=colour, attr=attr, bg=bg)

    def handle_input(self, screen):
        event = screen.get_event()
        if event:
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
        return True

    def tick(self, dt):
        self.player.process_action_queue(dt)

    def run(self):
        fps = 1 / 20
        with ManagedScreen() as screen:
            _continue = True
            while _continue:
                # clear screen buffer
                screen.clear_buffer(screen.COLOUR_WHITE, screen.A_NORMAL, screen.COLOUR_BLACK)

                # print command queue (idx 0 is the method, __name__ is the magic var for readable name)
                action_methods = ['%s %s,%s)' % (action[0].__name__, action[1][0], action[1][1]) for action in
                                  self.player.action_queue]
                screen.print_at('queue: %s' % ','.join(action_methods), 0, 1)
                screen.print_at('room: %s' % self.player.room, 0, 2)


                if self.player.fov_needs_update:
                    logger.debug('updating fov')
                    for idx_row, row in enumerate(self.player.room.map.map):
                        for idx_column, column in enumerate(self.player.room.map.map[idx_row]):
                            self.player.room.map.map[idx_row][idx_column].is_visible = False
                    fov(self.player.x, self.player.y, self.player.view_radius, self.player.room.map.update_visible)
                    self.player.fov_needs_update = False

                # render map, player is center
                for idx_row, row in enumerate(self.player.room.map.map):
                    for idx_column, column in enumerate(self.player.room.map.map[idx_row]):
                        tile_char = ' '
                        draw_colour = screen.COLOUR_WHITE
                        if self.player.room.map.map[idx_row][idx_column].is_visible:
                            tile_char = self.player.room.map.map[idx_row][idx_column].char
                            draw_colour = screen.COLOUR_WHITE
                        elif self.player.room.map.map[idx_row][idx_column].seen:
                            tile_char = self.player.room.map.map[idx_row][idx_column].char
                            draw_colour = screen.COLOUR_MAGENTA
                        self.screen_print_with_player_offset(screen, tile_char, idx_column, idx_row, colour=draw_colour)

                self.screen_print_with_player_offset(screen, self.player.char, self.player.x, self.player.y)

                # draw the screen!
                screen.refresh()

                # wait a bit
                sleep(fps)

                # process the actions further!
                self.tick(fps)

                # handle input
                _continue = self.handle_input(screen)


game = ScreenManager()
game.run()
