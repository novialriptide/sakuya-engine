"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from typing import Tuple, List
from copy import copy

import pygame
import math

from .entity import Entity
from .math import Vector

class Bullet(Entity):
    def __init__(
        self,
        angle: float = 0,
        speed: float = 4,
        color: Tuple[int, int, int] = (255, 255, 255),
        damage: float = 5,
        position: Vector = Vector(0, 0),
        obey_gravity: bool = False,
        custom_hitbox_size: Vector = Vector(0, 0),
        name: str = None,
        curve: float = 0
    ) -> None:
        super().__init__(
            position = position,
            obey_gravity = obey_gravity,
            custom_hitbox_size = custom_hitbox_size,
            name = name
        )
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage

        self.curve = curve

    def update(self, delta_time: float) -> None:
        angle = math.radians(self.angle)
        self.angle += self.curve * delta_time
        self.velocity = Vector(self.speed * math.cos(angle), self.speed * math.sin(angle))
        return super().update(delta_time)

class BulletSpawner:
    def __init__(
        self,
        assigned_entity: Entity,
        bullet: Bullet,
        entity_list: List[Entity],
        position_offset: Vector = Vector(0, 0),
        iterations: int = 1,
        total_bullet_arrays: int = 1,
        bullets_per_array: int = 1,
        spread_between_bullet_arrays: float = 1,
        spread_within_bullet_arrays: float = 1,
        starting_angle: float = 0,
        spin_rate: float = 0,
        spin_modificator: float = 0,
        invert_spin: bool = False,
        max_spin_rate: float = 1,
        fire_rate: float = 0,
        bullet_speed: float = 3,
        bullet_acceleration: float = 0,
        bullet_curve: float = 0,
        bullet_curve_change_rate: float = 0,
        invert_curve: bool = False,
        max_bullet_curve_rate: float = 1,
        bullet_lifetime: float = 3000
    ) -> None:
        """Constructor for BulletSpawner.

        This follows the Danmaku (弾幕) Theory.

        Parameters:
            starting_angle:
                The spawner's starting angle in radians.
            assigned_entity:
                The entity that will fire these bullets.
            position_offset:
                The position offset based on the assigned entity's position.
            bullet:
                The bullet the spawner will fire.
            entity_list:
                The list that the bullet will be added to.

            iterations:
                Total amount of iterations the spawner will go through. If set to 0, it will be infinite.
            total_bullet_arrays:
                Total amount of bullet-spawning arrays.
            bullets_per_array:
                Sets the amount of bullets within each array.
            spread_between_bullet_arrays:
                Sets the spread between individual bullet arrays. (in degrees)
            spread_within_bullet_arrays:
                Sets the spread within the bullet arrays.
                More specifically, it sets the spread between the 
                first and last bullet of each array. (in degrees)
            fire_rate:
                Set the bullet spawner's fire rate for each individual bullet.
            starting_angle:
                The starting angle (in degrees)
            spin_rate:
                This parameter sets the rate at which the
                bullet arrays will rotate around their origin.
            invert_spin / max_spin_rate:
                Nothing will happen if set to False, but if set to True, 
                the spin rate will invert once the spin rate has reached
                the max_spin_rate
            spin_modificator:
                The value that will be added to the spin_rate overtime.
            bullet_speed:
                The bullet's speed
            bullet_acceleration:
                This parameter sets the rate at which the
                bullet speed will change over time.
            bullet_curve:
                This parameter sets the curve at which
                the bullet will move along.
            bullet_curve_change_rate:
                This parameter sets the 
            invert_curve / max_bullet_curve_rate:
                Nothing will happen if set to False, but if set to True, 
                the curve rate will invert once the curve rate has reached
                the max_bullet_curve_rate
            bullet_lifetime:
                The bullet's lifetime in milliseconds.

        """
        self.next_fire_ticks = pygame.time.get_ticks()
        self.current_iteration = 0
        self.is_active = True
        self.angle = starting_angle
        # Args
        self.entity = assigned_entity
        self.entity.bullet_spawners.append(self)
        self.bullet = copy(bullet)
        self.entity_list = entity_list

        # Kwargs
        self.position_offset = position_offset
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
        self.bullet_curve_change_rate = bullet_curve_change_rate # wip
        self.invert_curve = invert_curve # wip
        self.max_bullet_curve_rate = max_bullet_curve_rate # wip
        self.bullet_lifetime = bullet_lifetime

    @property
    def total_bullets(self) -> int:
        return self.total_bullet_arrays * self.bullets_per_array

    @property
    def can_shoot(self) -> bool:
        return self.is_active and pygame.time.get_ticks() >= self.next_fire_ticks

    def shoot(self, angle: float) -> bool:
        """Shoot a bullet

        Parameters:
            angle: Angle to shoot the bullet.

        Returns:
            If True, a bullet has successfully been fired.
            More specifically, this returns BulletSpawner.can_shoot

        """
        bullet = copy(self.bullet)
        bullet.speed = self.bullet_speed
        bullet.angle = angle
        bullet.position = self.entity.position + self.position_offset
        bullet.acceleration = self.bullet_acceleration
        bullet.destroy(self.bullet_lifetime)
        bullet.curve = self.bullet_curve
        self.entity_list.append(bullet)

        return bullet

    def shoot_with_firerate(self, angle: float) -> None:
        if self.can_shoot:
            self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate
            self.shoot(angle)

    def update(self, delta_time: float) -> None:
        iter_bullet = 0
        if self.can_shoot:
            self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate

            spread_between_each_array = (self.spread_within_bullet_arrays 
            / self.total_bullet_arrays)
            spread_between_each_bullets = self.spread_between_bullet_arrays

            for a in range(self.total_bullet_arrays):
                for b in range(self.bullets_per_array):
                    angle = self.angle + spread_between_each_array * b + spread_between_each_bullets * a
                    self.shoot(angle)

                    iter_bullet += 1

            self.angle += self.spin_rate * delta_time
            self.spin_rate += self.spin_modificator * delta_time

        if iter_bullet >= self.total_bullets:
            self.current_iteration += 1

        if self.current_iteration >= self.iterations and self.iterations != 0:
            self.is_active = False

        if self.invert_spin:
            if self.spin_rate < -self.max_spin_rate:
                self.spin_rate = -self.max_spin_rate
                self.spin_modificator *= -1
            
            if self.spin_rate > self.max_spin_rate:
                self.spin_rate = self.max_spin_rate
                self.spin_modificator *= -1

    def draw_debug_angle(self, surface: pygame.Surface) -> None:
        """Draws a green or red line on surface to indicate 
        status and angle.

        Parameters:
            surface: Surface to draw on.

        """
        pass

def load_bullet_dict(data: dict) -> Bullet:
    if "custom_hitbox_size" in data.keys():
        data["custom_hitbox_size"] = Vector(
            data["custom_hitbox_size"][0],
            data["custom_hitbox_size"][1]
        )

    if "position" in data.keys():
        data["position"] = Vector(
            data["position"][0],
            data["position"][1]
        )
    
    return Bullet(**data)

def load_bulletspawner_dict(entity: Entity, entity_list: List[Entity], data: dict) -> BulletSpawner:
    bullet = load_bullet_dict(data["bullet"])
    del data["bullet"]

    if "position_offset" in data.keys():
        data["position_offset"] = Vector(
            data["position_offset"][0],
            data["position_offset"][1]
        )

    return BulletSpawner(entity, bullet, entity_list, **data)
