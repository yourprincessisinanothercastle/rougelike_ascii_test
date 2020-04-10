from asciimatics.screen import ManagedScreen
from time import sleep

from lib.world import World
from lib.world.creatures.player import Player

import logging
from lib.init_logging import init_logging

init_logging('debug')

logger=logging.getLogger(__name__)
logger.debug('test')

KEYS = dict(
    up=ord('w'),
    down=ord('s'),
    left=ord('a'),
    right=ord('d'),
    quit='q',
)


class ScreenManager:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.world.start_room.spawn_player(self.player)
        self.logs = []

    def add_log(self, *log):
        self.logs.append(log)
        self.logs = self.logs[:10]

    def screen_print_with_player_offset(self, screen, s, x, y):
        centre_x = (screen.width // 2) - self.player.x
        centre_y = (screen.height // 2) - self.player.y
        screen.print_at(s, centre_x + x, centre_y + y)

    def handle_input(self, screen):
        event = screen.get_event()
        if event:
            if event.key_code == ord(KEYS['quit']):
                return False
            if event.key_code == KEYS['up']:
                self.player.add_command(Player.DIRECTIONS['up'])
            if event.key_code == KEYS['down']:
                self.player.add_command(Player.DIRECTIONS['down'])
            if event.key_code == KEYS['left']:
                self.player.add_command(Player.DIRECTIONS['left'])
            if event.key_code == KEYS['right']:
                self.player.add_command(Player.DIRECTIONS['right'])
        return True

    def handle_player_command_queue(self):
        command = self.player.get_next_command()
        if command:
            if command == Player.DIRECTIONS['up']:
                self.player.move(0, -1)
            if command == Player.DIRECTIONS['down']:
                self.player.move(0, 1)
            if command == Player.DIRECTIONS['left']:
                self.player.move(-1, 0)
            if command == Player.DIRECTIONS['right']:
                self.player.move(1, 0)

    def tick(self):
        self.handle_player_command_queue()

    def run(self):
        fps = 1 / 20
        tick_length = .25
        with ManagedScreen() as screen:
            _continue = True
            dt = 0
            while _continue:
                screen.clear_buffer(screen.COLOUR_WHITE, screen.A_NORMAL, screen.COLOUR_BLACK)
                screen.print_at('tick: %s' % dt, 0, 0)
                screen.print_at('queue: %s' % ','.join(self.player.command_queue), 0, 1)
                for idx, log in enumerate(self.logs):
                    screen.print_at(log, 0, 3 + idx)
                
                for idx, line in enumerate(self.player.room.map.draw()):
                    self.screen_print_with_player_offset(screen, line, 0, idx)
                self.screen_print_with_player_offset(screen, self.player.char, self.player.x, self.player.y)
                screen.refresh()

                sleep(fps)

                dt += fps
                if dt >= tick_length:
                    self.tick()
                    dt = dt % tick_length
                _continue = self.handle_input(screen)


game = ScreenManager()
game.run()
