from asciimatics.screen import ManagedScreen
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

    def screen_print_with_player_offset(self, screen, s, x, y):
        centre_x = (screen.width // 2) - self.player.x
        centre_y = (screen.height // 2) - self.player.y
        screen.print_at(s, centre_x + x, centre_y + y)

    def handle_input(self, screen):
        event = screen.get_event()
        if event:
            if event.key_code == ord(QUIT):
                return False
            if event.key_code == ord(UP):
                self.player.add_command(UP)
            if event.key_code == ord(DOWN):
                self.player.add_command(DOWN)
            if event.key_code == ord(LEFT):
                self.player.add_command(LEFT)
            if event.key_code == ord(RIGHT):
                self.player.add_command(RIGHT)
        return True

    def handle_player_command_queue(self):
        command = self.player.get_next_command()
        if command:
            if command == UP:
                self.player.move(0, -1)
            if command == DOWN:
                self.player.move(0, 1)
            if command == LEFT:
                self.player.move(-1, 0)
            if command == RIGHT:
                self.player.move(1, 0)

    def tick(self):
        self.handle_player_command_queue()

    def run(self):
        fps = 1 / 20
        tick_length = .5
        with ManagedScreen() as screen:
            _continue = True
            dt = 0
            while _continue:
                screen.clear_buffer(screen.COLOUR_WHITE, screen.A_NORMAL, screen.COLOUR_BLACK)
                screen.print_at('tick: %s' % dt, 0, 0)
                screen.print_at('queue: %s' % ','.join(self.player.command_queue), 0, 1)
                for idx, line in enumerate(self.player.room.map.draw()):
                    self.screen_print_with_player_offset(screen, line, 0, idx)
                self.screen_print_with_player_offset(screen, '@', self.player.x, self.player.y)
                screen.refresh()

                sleep(fps)

                dt += fps
                if dt >= tick_length:
                    self.tick()
                    dt = dt % tick_length
                _continue = self.handle_input(screen)


game = ScreenManager()
game.run()
