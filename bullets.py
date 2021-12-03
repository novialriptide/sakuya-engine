"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""

from .entity import Entity
from .math import Vector

class Bullet(Entity):
    def __init__(self):
        pass

class BulletSpawner:
    def __init__(self, speed: float, frequency: float, starting_angle: float) -> None:
        """Constructor for BulletSpawner.
        
        This follows the Danmaku (弾幕) Theory.

        Parameters:
            speed: The bullet's default speed.
            frequency: The bullet's spawn rate frequency.
            starting_angle: The spawner's starting angle in radians.

        """
        pass

    def spawn_bullet(self, acceleration: float) -> Bullet:
        pass

    def move_angle(self, new_angle: float, speed: float):
        pass