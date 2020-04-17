import logging
import random
from typing import TYPE_CHECKING

from lib.world.creatures._creature import Creature

if TYPE_CHECKING:
    from main import ScreenManager

logger = logging.getLogger(__name__)


class Animation:
    def setup_animation(self, time_per_frame, frames, colour=7):
        self.time_per_frame = time_per_frame
        self.animation_frames = frames
        self.state_timer = 0

        self.complete_animation_time = len(self.animation_frames) * self.time_per_frame

        self.colour = colour

    def animate(self, screen_manager, dt, offset_x, offset_y, x, y):

        self.state_timer += dt
        logger.debug('timer %s' % self.state_timer)

        if self.state_timer > self.complete_animation_time:
            step = len(self.animation_frames) - 1
        else:
            step = int(self.state_timer // self.time_per_frame)

        logger.debug(step)
        shape = self.animation_frames[step]
        self.draw_shape(screen_manager, shape, offset_x, offset_y, x, y, colour=self.colour)


class Explosion(Creature, Animation):
    CHARS = dict(
        up='^',
        down='v',
        left='<',
        right='>',
    )

    animation_frames = [
        [
            'OoO',
            'oOo',
            'OoO'
        ],
        [
            'oOo',
            '00O',
            'o0o'
        ],
        [
            'OOo',
            'O0o',
            'oOo'
        ],
        [
            'o0o',
            'oOo',
            'ooo'
        ],
        [
            'oOo',
            'ooo',
            'ooo'
        ],
    ]

    def __init__(self):
        super().__init__(0, 0)

        frame_time = .2
        self.ACTION_TIME = dict(
            die=frame_time * len(Explosion.animation_frames)
        )
        self.setup_animation(frame_time, Explosion.animation_frames, colour=random.randint(0,254))

    def draw_shape(self, screen_manager, shape, offset_x, offset_y, x, y, colour=7):
        for idx_line, line in enumerate(shape):
            for idx_column, char in enumerate(line):
                _x = x + offset_x + idx_column
                _y = y + offset_y + idx_line
                screen_manager.screen_print_with_player_offset(char, _x, _y, colour=colour)

    def draw(self, screen_manager, dt=0):
        screen_manager: ScreenManager
        self.animate(screen_manager, dt, -1, -1, self.x, self.y)

    def die(self):
        self.room.remove_creature(self)
