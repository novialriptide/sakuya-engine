"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from typing import Tuple
from copy import copy

import pygame
import math

from .entity import Entity
from .math import Vector

class Bullet(Entity):
    def __init__(
        self,
        position: Vector,
        angle: float,
        speed: float,
        color: Tuple[int, int, int],
        damage: float,
        obey_gravity: bool = False,
        custom_hitbox_size: Vector = Vector(0, 0),
        name: str = None
    ) -> None:
        super().__init__(
            None,
            position,
            obey_gravity = obey_gravity,
            custom_hitbox_size = custom_hitbox_size,
            name = name
        )
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage

    @property
    def sprite(self):
        """Returns a circle with a hole at its end to indicate its direction and angle.
        """
        pass

    def update(self, delta_time: float) -> None:
        self.velocity = Vector(self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
        return super().update(delta_time)

class BulletSpawner:
    def __init__(
        self,
        assigned_entity: Entity,
        position_offset: Vector,
        bullet: Bullet,
        iterations: int = 1,
        total_bullet_arrays: int = 1,
        bullets_per_array: int = 1,
        spread_between_bullet_arrays: float = 1,
        spread_within_bullet_arrays: float = 1,
        starting_angle: float = 0,
        spin_rate: float = 1,
        spin_modificator: float = 0,
        invert_spin: bool = False,
        max_spin_rate: float = 1,
        fire_rate: float = 0,
        bullet_speed: float = 3,
        bullet_acceleration: float = 0,
        bullet_curve: float = 0,
        bullet_lifetime: float = 3000
    ) -> None:
        """Constructor for BulletSpawner.

        This follows the Danmaku (弾幕) Theory.

        Parameters:
            starting_angle: The spawner's starting angle in radians.
            assigned_entity: The entity that will fire these bullets.
            position_offset: The position offset based on the assigned entity's position.
            bullet: The bullet the spawner will fire.

            iterations:
                Total amount of iterations the spawner will go through. If set to 0, it will be infinite.
            total_bullet_arrays:
                Total amount of bullet-spawning arrays.
            bullets_per_array:
                Sets the amount of bullets within each array.
            spread_between_bullet_arrays:
                Sets the spread between individual bullet arrays. (in radians)
            spread_within_bullet_arrays:
                Sets the spread within the bullet arrays.
                More specifically, it sets the spread between the 
                first and last bullet of each array. (in radians)
            fire_rate:
                Set the bullet spawner's fire rate for each individual bullet.
            starting_angle:
                The starting angle (in radians)
            spin_rate:
                This parameter sets the rate at which the
                bullet arrays will rotate around their origin.
            invert_spin / max_spin_rate:
                Nothing will happen if set to False, but if set to True, 
                the spin rate will invert once the spin rate has reached
                the max_spin_rate
            bullet_speed:
                The bullet's speed
            bullet_acceleration:
                This parameter sets the rate at which the
                bullet speed will change over time.
            bullet_curve:
                This parameter sets the curve at which
                the bullet will move along.
            bullet_lifetime:
                The bullet's lifetime in milliseconds.

        """
        self.next_fire_ticks = pygame.time.get_ticks()
        self.current_iteration = 0
        self.current_bullet = 0
        self.is_active = True
        # Args
        self.angle = starting_angle
        self.entity = assigned_entity
        self.position_offset = position_offset
        self.bullet = copy(bullet)

        # Kwargs
        self.iterations = iterations
        self.total_bullet_arrays = total_bullet_arrays
        self.bullets_per_array = bullets_per_array
        self.spread_between_bullet_arrays = spread_between_bullet_arrays
        self.spread_within_bullet_arrays = spread_within_bullet_arrays
        self.starting_angle = starting_angle
        self.spin_rate = spin_rate
        self.spin_modificator = spin_modificator
        self.invert_spin = invert_spin
        self.max_spin_rate = max_spin_rate
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.bullet_acceleration = bullet_acceleration
        self.bullet_curve = bullet_curve
        self.bullet_lifetime = bullet_lifetime

    @property
    def total_bullets(self) -> int:
        return self.total_bullet_arrays * self.bullets_per_array

    @property
    def can_shoot(self) -> bool:
        return self.is_active and pygame.time.get_ticks() >= self.next_fire_ticks

    def shoot(self) -> bool:
        """Shoot a bullet

        Returns:
            If True, a bullet has successfully been fired.
            More specifically, this returns BulletSpawner.can_shoot

        """
        if self.can_shoot:
            self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate
            print(self.next_fire_ticks)

        return self.can_shoot

    def update(self, delta_time: float) -> None:
        # it will keep trying to shoot the current_bullet
        # keep checking if can_shoot is valid and if it is then it will update the current_bullet.
        if self.can_shoot:
            spread_between_each_array = self.spread_within_bullet_arrays / self.total_bullet_arrays
            spread_between_each_bullets = self.spread_between_bullet_arrays / self.bullets_per_array

            iter_bullet = 0
            for a in range(self.total_bullet_arrays):
                for b in range(self.bullets_per_array):
                    iter_bullet += 1
                    if iter_bullet == self.current_bullet:
                        self.shoot()

            self.current_bullet += 1

        if self.current_bullet >= self.total_bullets:
            self.current_bullet = 0

    def draw_debug_angle(self, surface: pygame.Surface) -> None:
        """Draws a green or red line on surface to indicate 
        status and angle.

        Parameters:
            surface: Surface to draw on.

        """
        pass