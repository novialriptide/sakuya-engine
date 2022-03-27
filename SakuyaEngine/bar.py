"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .math import move_toward


class Bar:
    def __init__(self, max_val, update_speed, init_val: float = 0):
        """
        :param float max_health:

        In order for this to work properly, set the current_health
        value to whatever the health of the boss will be.
        """
        self.max_val = max_val
        self.current_val = init_val
        self._display_val = init_val
        self.update_speed = update_speed

    @property
    def display_val(self):
        return self._display_val

    def update(self, delta_time: float):
        self._display_val = move_toward(
            self._display_val, self.current_val, self.update_speed * delta_time
        )
