from pygame.time import get_ticks

from Scripts.Utility.cronos_clock import CronosClock
from Scripts.animation import Animation


class Action:

    def __init__(self, animation: Animation, cooldown: float):

        self.timer = CronosClock()

        self.animation = animation

        self.cooldown = cooldown

    def attempt(self):
        print(self.timer.has_seconds_passed(self.animation.display_duration/1000 + self.cooldown))
        if self.timer.has_seconds_passed(self.animation.display_duration/1000 + self.cooldown):
            self.animation.start_animation()
            self.timer.restart_time()

    def draw(self):

        # Animation Type Diff
        if self.animation.start_time is not None:
            _elapsed_time = get_ticks() - self.animation.start_time
        else:
            _elapsed_time = 0

        # Run the animation and get the current frame
        self.animation.run_once(_elapsed_time)
