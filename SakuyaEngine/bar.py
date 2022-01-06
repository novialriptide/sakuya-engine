"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .math import move_toward

class Bar:
    def __init__(self, max_health, update_speed):
        """
        :param float max_health:

        In order for this to work properly, set the current_health 
        value to whatever the health of the boss will be. 
        """
        self.max_health = max_health
        self.current_health = max_health
        self._display_health = max_health
        self.update_speed = update_speed

    @property
    def display_health(self):
        return self._display_health

    def update(self, delta_time: float):
        self._display_health = move_toward(self._display_health, self.current_health, self.update_speed * delta_time)