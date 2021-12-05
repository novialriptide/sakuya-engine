"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""

from typing import Tuple, List

from .entity import Entity
from .math import Vector

class Bullet(Entity):
    def __init__(
        self,
        position: Vector,
        angle: float,
        speed: float,
        color: Tuple(int, int, int),
        damage: float
    ) -> None:
        self.position = position
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage

class BulletSpawner:
    def __init__(
        self,
        starting_angle: float,
        speed: float, 
        frequency: float,
        assigned_entity: Entity,
        position_offset: Vector
    ) -> None:
        """Constructor for BulletSpawner.
        
        This follows the Danmaku (弾幕) Theory.

        Parameters:
            starting_angle: The spawner's starting angle in radians.
            speed: The bullet's default speed.
            frequency: The bullet's spawn rate frequency.

        """
        self.starting_angle = starting_angle
        self.speed = speed
        self.frequency = frequency
        self.entity = assigned_entity
        self.position_offset = position_offset

    def spawn_bullet(self, acceleration: Vector) -> Bullet:
        pass

    def move_angle(self, new_angle: float, speed: float):
        pass