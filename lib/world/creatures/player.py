import logging
from typing import List, Tuple

from lib.world.creatures._creature import Creature

logger = logging.getLogger(__name__)


class Player(Creature):
    DIRECTIONS = dict(
        up='up',
        down='down',
        left='left',
        right='right',
    )

    CHARS = dict(
        up='◓',
        down='◒',
        left='◐',
        right='◑',
    )

    ACTION_TIME = dict(
        move=.10,
        hit=.20
    )

    def __init__(self):
        super().__init__()
        self.action_queue: List[Tuple] = []
        self.direction = Player.DIRECTIONS['left']

        self.current_action: Tuple = ()  # ( method, (args,) )
        self.current_action_time: int = 0

    @property
    def char(self):
        return Player.CHARS[self.direction]

    def process_action_queue(self, time_delta: float):
        """
        progress current action further, or poll for new action
        """
        
        if self.current_action:
            # get action time from dict
            action_time = Player.ACTION_TIME[self.current_action[0].__name__]

            # add time delta to current_action_time
            self.current_action_time += time_delta

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
                
    def add_action(self, method, *args, **kwargs):
        action = (method, (args, kwargs))
        logger.debug(action)
        self.action_queue.append(action)

    def move(self, dx, dy):
        target_tile = self.room.map.map[self.y + dy][self.x + dx]
        if dx > 0:
            new_direction = Player.DIRECTIONS['right']
        elif dx < 0:
            new_direction = Player.DIRECTIONS['left']
        elif dy > 0:
            new_direction = Player.DIRECTIONS['down']
        else:
            new_direction = Player.DIRECTIONS['up']

        if self.direction != new_direction:
            self.direction = new_direction
            return

        if not target_tile.blocked:
            self.x += dx
            self.y += dy
