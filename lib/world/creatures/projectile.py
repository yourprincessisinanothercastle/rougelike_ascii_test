import logging
import random
from typing import TYPE_CHECKING

from lib.world.creatures._creature import Creature
from lib.world.creatures.explosion import Explosion

if TYPE_CHECKING:
    from main import ScreenManager

logger = logging.getLogger(__name__)


class Projectile(Creature):
    CHARS = dict(
        up='^',
        down='v',
        left='<',
        right='>',
    )

    ACTION_TIME = dict(
        move=.05
    )

    def __init__(self):
        super().__init__(0, 0)
        self.direction = Creature.DIRECTIONS['left']

        self.fov_needs_update = True
        self.view_radius = 4

        self.speed = 1
        self.accuracy = 1
        self.strength = 1

    @property
    def char(self,):
        return Projectile.CHARS[self.direction]

    def draw(self, screen_manager, dt=0):
        screen_manager: ScreenManager
        screen_manager.screen_print_with_player_offset(self.char, self.x, self.y, colour=random.randint(0, 254))
        pass

    def process_action_queue(self, time_delta: float):
        """
        progress current action further, or poll for new action
        """

        if self.current_action:
            # get action time from dict
            action_time = Projectile.ACTION_TIME[self.current_action[0].__name__]

            # add time delta to current_action_time
            self.current_action_time += time_delta
            logger.debug('current action time: %s' % self.current_action_time)

            if self.current_action_time >= action_time:
                # unpack current_action
                action, (args, kwargs) = self.current_action

                # execute
                action(*args, **kwargs)

                if self.action_queue:
                    # get the next action
                    self.current_action = self.action_queue.pop(0)

                    # set current_action_time to whats left of the last time slot
                    self.current_action_time = self.current_action_time % action_time
                else:
                    self.current_action = None

        else:
            if self.action_queue:
                self.current_action = self.action_queue.pop(0)
                self.current_action_time = 0

    def shoot(self, direction):
        self.direction = direction
        if direction == Creature.DIRECTIONS['right']:
            self.add_action(self.move, 1, 0)
        elif direction == Creature.DIRECTIONS['left']:
            self.add_action(self.move, -1, 0)
        elif direction == Creature.DIRECTIONS['down']:
            self.add_action(self.move, 0, 1)
        else:
            self.add_action(self.move, 0, -1)

    def explode(self):
        explosion = Explosion()
        self.room.spawn_creature(explosion, self.x, self.y)
        explosion.add_action(explosion.die)
        self.room.remove_creature(self)

    def move(self, dx, dy):
        target_tile = self.room.map.tiles[self.y + dy][self.x + dx]

        if not target_tile.blocked:
            self.x += dx
            self.y += dy
            self.add_action(self.move, dx, dy)
        else:
            self.explode()
