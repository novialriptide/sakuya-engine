"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import Tuple, List, TypeVar, Callable
from copy import copy
from .clock import Clock

import pygame
import math

from .entity import Entity
from .animation import split_image
from .math import get_angle

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.math.Vector2)

class Bullet(Entity):
    def __init__(
        self,
        angle: float = 0,
        speed: float = 4,
        color: Tuple[int, int, int] = (255, 255, 255),
        damage: float = 5,
        position: pygame_vector2 = pygame.math.Vector2(0, 0),
        obey_gravity: bool = False,
        custom_hitbox_size: pygame_vector2 = pygame.math.Vector2(0, 0),
        name: str = None,
        static_sprite: pygame.Surface = None,
        curve: float = 0,
        tags: List[str] = [],
        sound_upon_fire = None,
        clock: Clock or None = None
    ) -> None:
        super().__init__(
            position = position,
            obey_gravity = obey_gravity,
            custom_hitbox_size = custom_hitbox_size,
            name = name,
            static_sprite = static_sprite,
            clock = clock
        )
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage
        self.curve = curve
        self.tags = tags
        self.direction = 0
        self._sprite = static_sprite
        self.sound_upon_fire = sound_upon_fire
        
        s = self.sprite
        if s is not None:
            self._sprite_width, self._sprite_height = s.get_size()
        else:
            r = self.rect
            self._sprite_width, self._sprite_height = r.width, r.height

    @property
    def sprite(self) -> pygame.Surface:
        if self._sprite is None:
            return None

        direction = -self.angle + 360
        if self.direction != direction:
            self._sprite = pygame.transform.rotate(super().sprite, direction)
            self.direction = direction

        return self._sprite

    @property
    def custom_hitbox(self) -> pygame.Rect:
        hb_size = self.custom_hitbox_size
        self._custom_hitbox_rect.x = self.position.x + self._sprite_width/2 - hb_size.x
        self._custom_hitbox_rect.y = self.position.y + self._sprite_height/2 - hb_size.y
        self._custom_hitbox_rect.width = hb_size.x*2
        self._custom_hitbox_rect.height = hb_size.y*2
        return self._custom_hitbox_rect

    def update(self, delta_time: float) -> None:
        angle = math.radians(self.angle)
        self.angle += self.curve * delta_time
        self.velocity = pygame.Vector2(self.speed * math.cos(angle), self.speed * math.sin(angle))
        return super().update(delta_time)

class BulletSpawner:
    def __init__(
        self,
        bullet: Bullet,
        clock: Clock = None,
        position: pygame_vector2 = pygame.Vector2(0, 0),
        position_offset: pygame_vector2 = pygame.Vector2(0, 0),
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
        bullet_lifetime: float = 3000,
        aim: bool = False,
        target: Entity = None,
        is_active: bool = False,
        repeat: bool = False,
        wait_until_reset: int = 0
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
        self._clock = clock
        
        if self._clock is None:
            self.next_fire_ticks = pygame.time.get_ticks()
            self.next_reset_ticks = pygame.time.get_ticks()
        else:
            self.next_fire_ticks = self._clock.get_time()
            self.next_reset_ticks = self._clock.get_time()
        self.waiting_reset = False
        self.current_iteration = 0
        self.angle = starting_angle
        # Args
        self.bullet = copy(bullet)

        # Kwargs
        self.position = position
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
        self.aim = aim
        self.target = target
        self.is_active = is_active
        self.repeat = repeat # wip
        self.wait_until_reset = wait_until_reset # wip

    @property
    def clock(self) -> Clock:
        return self._clock
    
    @clock.setter
    def clock(self, value: Clock) -> None:
        self._clock = value
        self.next_fire_ticks = self._clock.get_time()
        self.next_reset_ticks = self._clock.get_time()

    @property
    def total_bullets(self) -> int:
        return self.total_bullet_arrays * self.bullets_per_array

    @property
    def can_shoot(self) -> bool:
        if self._clock is None:
            return self.is_active and pygame.time.get_ticks() >= self.next_fire_ticks
        else:
            return self.is_active and self._clock.get_time() >= self.next_fire_ticks

    @property
    def can_reset(self) -> bool:
        if self._clock is None:
            return self.repeat and pygame.time.get_ticks() >= self.next_reset_ticks
        else:
            return self.repeat and self._clock.get_time() >= self.next_reset_ticks

    def shoot(self, angle: float) -> Bullet:
        """Shoot a bullet.

        Parameters:
            angle: Angle to shoot the bullet.

        """
        bullet = copy(self.bullet)
        bullet.speed = self.bullet_speed
        bullet.angle = angle
        bullet.position = self.position + self.position_offset - bullet.center_offset
        bullet.acceleration = self.bullet_acceleration
        bullet.curve = self.bullet_curve
        bullet.clock = self._clock
        bullet.destroy(self.bullet_lifetime)
        
        soundfx = bullet.sound_upon_fire
        if soundfx is not None:
            pygame.mixer.Sound.play(soundfx)


        return bullet

    def shoot_with_firerate(self, angle: float) -> Bullet:
        """Shoot a bullet with a fire rate limit.

        Parameters:
            angle: Angle to shoot the bullet.

        """
        if self.can_shoot:
            if self._clock is None:
                self.next_fire_ticks = pygame.time.get_ticks() + self.fire_rate
            else:
                self.next_fire_ticks = self._clock.get_time() + self.fire_rate
            return self.shoot(angle)

    def update(self, delta_time: float) -> List[Bullet]:
        iter_bullet = 0
        bullets = []
        if self._clock is None:
            pg_ticks = pygame.time.get_ticks()
        else:
            pg_ticks = self._clock.get_time()
        if self.can_shoot:
            self.next_fire_ticks = pg_ticks + self.fire_rate
            spread_between_each_array = (self.spread_within_bullet_arrays / self.total_bullet_arrays)
            spread_between_each_bullets = self.spread_between_bullet_arrays

            center_angle = ((self.total_bullet_arrays - 1) * spread_between_each_bullets + (self.bullets_per_array - 1) * spread_between_each_array) / 2
            for a in range(self.total_bullet_arrays):
                for b in range(self.bullets_per_array):
                    angle = self.angle + spread_between_each_array * b + spread_between_each_bullets * a
                    if self.target is not None and self.aim:
                        # Responsible for making the bullet arrays aim from their center.
                        target_angle = math.degrees(get_angle(self.position, self.target.position + self.target.center_offset)) - center_angle
                        angle += target_angle
                    bullets.append(self.shoot(angle))

                    iter_bullet += 1

            self.angle += self.spin_rate * delta_time
            self.spin_rate += self.spin_modificator * delta_time


        if iter_bullet >= self.total_bullets:
            self.current_iteration += 1

        if self.current_iteration > self.iterations - 1 and self.iterations != 0:
            self.current_iteration = 0
            self.is_active = False

        if self.invert_spin:
            if self.spin_rate < -self.max_spin_rate:
                self.spin_rate = -self.max_spin_rate
                self.spin_modificator *= -1
            
            if self.spin_rate > self.max_spin_rate:
                self.spin_rate = self.max_spin_rate
                self.spin_modificator *= -1

        if self.repeat and not self.is_active and not self.waiting_reset:
            self.next_reset_ticks = pg_ticks + self.wait_until_reset
            self.waiting_reset = True
        
        if self.can_reset and self.repeat and not self.is_active:
            self.current_iteration = 0
            self.waiting_reset = False
            self.is_active = True
        
        return bullets

def load_bullet_dict(data: dict) -> Bullet:
    if "custom_hitbox_size" in data.keys():
        data["custom_hitbox_size"] = pygame.Vector2(data["custom_hitbox_size"])

    if "position" in data.keys():
        data["position"] = pygame.Vector2(data["position"])

    if "static_sprite" in data.keys():
        ss_data = data["static_sprite"]
        sprites = split_image(
            pygame.image.load(ss_data["path"]),
            px_width = ss_data["width"],
            px_height = ss_data["height"]
        )
        index = ss_data["index"]
        data["static_sprite"] = sprites[index]

    return Bullet(**data)

def load_bulletspawner_dict(data: dict) -> BulletSpawner:
    bullet = load_bullet_dict(data["bullet"])
    del data["bullet"]

    if "position_offset" in data.keys():
        data["position_offset"] = pygame.Vector2(data["position_offset"])

    return BulletSpawner(bullet, **data)
