"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from __future__ import annotations
from typing import TypeVar, Callable

import pygame

from typing import List
from copy import copy

from .clock import Clock
from .animation import Animation
from .physics import gravity
from .controllers import BaseController
from .effect_particles import Particles
from .bar import Bar
from .math import vector2_move_toward

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)


class Entity:
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: int = 1,
        max_health: float = 100,
        position: pygame_vector2 = pygame.Vector2(0, 0),
        controller: BaseController = None,
        has_collision: bool = True,
        has_rigidbody: bool = False,
        enable_terminal_velocity: bool = False,
        obey_gravity: bool = False,
        speed: float = 0,
        custom_hitbox_size: pygame_vector2 = pygame.Vector2(0, 0),
        particle_systems: List[Particles] = [],
        bullet_spawners: List[BulletSpawner] = [],
        update_bullet_spawners: bool = True,
        static_sprite: pygame.Surface = None,
        healthbar_update_speed: float = 1000,
        healthbar_position_offset: pygame_vector2 = pygame.Vector2(0, 0),
        draw_healthbar: bool = True,
        target_position: pygame_vector2 or None = None,
        destroy_position: pygame_vector2 or None = None,
        disable_bulletspawner_while_movement: bool = True,
        clock: Clock or None = None,
        gravity_scale: float = 1,
    ):
        self._clock = None

        self.name = name
        self.tags = tags
        self.scale = pygame.Vector2(1, 1) * scale

        # Animations
        self.animations = {}
        self.current_anim = None

        # Positions & Movement
        self.position = position
        self.target_position = target_position

        # Controller
        if controller is not None:
            self.controller = controller()
        if controller is None:
            self.controller = None

        # Collisions & Physics
        self.has_collision = has_collision
        self.has_rigidbody = has_rigidbody
        self.obey_gravity = obey_gravity
        self.enable_terminal_velocity = enable_terminal_velocity
        self.custom_hitbox_size = custom_hitbox_size
        self.speed = speed
        self.terminal_velocity = 10.0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._custom_hitbox_rect = pygame.Rect(0, 0, 0, 0)
        self.gravity_scale = gravity_scale

        # Systems
        self.particle_systems = particle_systems
        self.bullet_spawners = bullet_spawners
        self.update_bullet_spawners = update_bullet_spawners
        self.disable_bulletspawner_while_movement = disable_bulletspawner_while_movement

        # Destroy
        self._destroy_val = 0
        self._enable_destroy = False
        self._destroy_queue = False
        self.destroy_position = destroy_position
        self.points_upon_death = 0

        # Health
        self.current_health = max_health
        self.max_health = max_health

        # Health Bar
        self.healthbar = Bar(max_health, healthbar_update_speed)
        self.healthbar_position_offset = healthbar_position_offset
        self.draw_healthbar = draw_healthbar

        self.static_sprite = static_sprite

    @property
    def clock(self) -> Clock:
        return self._clock

    @clock.setter
    def clock(self, value: Clock) -> None:
        self._clock = value
        self.next_fire_ticks = self._clock.get_time()
        self.next_reset_ticks = self._clock.get_time()

    @property
    def sprite(self) -> pygame.Surface:
        if self.static_sprite is not None:
            if self.scale.x != 1 or self.scale.y != 1:
                width, height = self.static_sprite.get_size()
                scaled_sprite = pygame.transform.scale(
                    self.static_sprite, (self.scale.x * width, self.scale.y * height)
                )
                return scaled_sprite
            else:
                return self.static_sprite

        cur_anim = self.anim_get(self.current_anim)
        if cur_anim is not None:
            if self.scale.x != 1 or self.scale.y != 1:
                width, height = cur_anim.sprite.get_size()
                scaled_sprite = pygame.transform.scale(
                    cur_anim.sprite, (self.scale.x * width, self.scale.y * height)
                )
                return scaled_sprite
            else:
                return cur_anim.sprite

    @property
    def rect(self) -> pygame.Rect:
        if self.sprite is not None:
            width, height = self.sprite.get_size()
            self._rect.x = self.position.x
            self._rect.y = self.position.y
            self._rect.width = width
            self._rect.height = height
        if self.sprite is None:
            self._rect.x = self.position.x
            self._rect.y = self.position.y
            self._rect.width = 1
            self._rect.height = 1
        return self._rect

    @property
    def custom_hitbox(self) -> pygame.Rect:
        s = self.sprite
        if s is not None:
            width, height = s.get_size()
        else:
            r = self.rect
            width, height = r.width, r.height
        hb_size = self.custom_hitbox_size
        self._custom_hitbox_rect.x = self.position.x + width / 2 - hb_size.x
        self._custom_hitbox_rect.y = self.position.y + height / 2 - hb_size.y
        self._custom_hitbox_rect.width = hb_size.x * 2
        self._custom_hitbox_rect.height = hb_size.y * 2
        return self._custom_hitbox_rect

    @property
    def center_offset(self) -> pygame.Vector2:
        s = self.sprite
        if s is not None:
            width, height = s.get_size()
        else:
            r = self.rect
            width, height = r.width, r.height
        return pygame.Vector2(width / 2, height / 2)

    @property
    def center_position(self) -> pygame.Vector2:
        width, height = self.sprite.get_size()
        return self.position + pygame.Vector2(width / 2, height / 2)

    def destroy(self, time: int) -> None:
        """Set the destruction time.

        Parameters:
            time: milliseconds to destruction

        """
        self._enable_destroy = True
        if self._clock is None:
            self._destroy_val = time + pygame.time.get_ticks()
        else:
            self._destroy_val = time + self._clock.get_time()

    def move(
        self, movement: pygame_vector2, collision_rects: List[pygame.Rect]
    ) -> bool:
        """Moves the position

        Parameters:
            movement: value to add to position

        Returns:
            If true, the position has been updated

        """
        hit = {"top": False, "bottom": False, "left": False, "right": False}
        self.position.x += movement.x
        test_rect = self.rect.copy()
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)

        for c in verified_collisions:
            if movement.x > 0:
                test_rect.right = c.left
                self.position.x = test_rect.x
                hit["right"] = True
            if movement.x < 0:
                test_rect.left = c.right
                self.position.x = test_rect.x
                hit["left"] = True

        self.position.y += movement.y
        test_rect = self.rect.copy()
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)
        for c in verified_collisions:
            if movement.y > 0:
                test_rect.bottom = c.top
                self.position.y = test_rect.y
                hit["top"] = True
            if movement.y < 0:
                test_rect.top = c.bottom
                self.position.y = test_rect.y
                hit["bottom"] = True

        return hit

    def anim_get(self, animation_name: str) -> Animation:
        if animation_name is not None:
            return self.animations[animation_name]
        if animation_name is None:
            return None

    def anim_set(self, animation_name: str) -> bool:
        """Assign an animation to be played

        Parameters:
            animation_name: Animation to be played

        Returns:
            If true, playing the animation was successful

        """
        self.current_anim = animation_name

    def anim_add(self, animation: Animation) -> None:
        """Adds an animation

        Parameters:
            animation: Animation to be added

        """
        self.animations[animation.name] = copy(animation)

    def anim_remove(self, animation_name: str) -> bool:
        """Removes an animation

        Parameters:
            animation_name: Animation to be removed

        Returns:
            If True, removing the animation was successful

        """
        raise NotImplementedError

    def copy(self) -> Entity:
        """Returns a copy of the entity

        You should not use Python3's copy.copy() method since
        it will interfere with the same entities animations

        """
        e = copy(self)
        new_anims = {}
        new_particles = []
        new_bullet_spawners = []
        new_healthbar = copy(e.healthbar)
        for a in self.animations.keys():
            new_anims[a] = copy(self.anim_get(a))

        for p in self.particle_systems:
            new_particles.append(copy(p))

        for bs in self.bullet_spawners:
            new_bullet_spawners.append(copy(bs))

        e.animations = new_anims
        e.particle_systems = new_particles
        e.bullet_spawners = new_bullet_spawners
        e.healthbar = new_healthbar

        return e

    def update(
        self, delta_time: float, collision_rects: List[pygame.Rect] = []
    ) -> None:
        """Updates the position, animation, etc

        Parameters:
            delta_time: the game's delta time

        """
        # Destroy
        if self._clock is None:
            if self._enable_destroy and self._destroy_val <= pygame.time.get_ticks():
                self._destroy_queue = True
        else:
            if self._enable_destroy and self._destroy_val <= self._clock.get_time():
                self._destroy_queue = True

        if self.destroy_position == self.position:
            self._destroy_queue = True

        # Update Particles
        for ps in self.particle_systems:
            ps.position = self.position
            ps.update(delta_time)

        # Update Animation
        if self.current_anim is not None:
            self.anim_get(self.current_anim).update(delta_time)

        # Update HealthBar
        self.healthbar.current_health = self.current_health
        self.healthbar.update(delta_time)

        # Update bullet spawners
        for b in self.bullet_spawners:
            if self._clock is not None and b.clock is None:
                b.clock = self._clock

        # Apply terminal velocity
        term_vec = self.terminal_velocity * delta_time
        if self.enable_terminal_velocity:
            if self.velocity.x < 0:
                self.velocity.x = max(self.velocity.x, term_vec)
            if self.velocity.x > 0:
                self.velocity.x = min(self.velocity.x, term_vec)
            if self.velocity.y < 0:
                self.velocity.y = max(self.velocity.y, term_vec)
            if self.velocity.y > 0:
                self.velocity.y = min(self.velocity.y, term_vec)

        # Controller movement
        if self.controller is not None:
            self.velocity = self.controller.movement * self.speed

        g = gravity
        if not self.obey_gravity:
            g = pygame.Vector2(0, 0)

        # Apply velocity
        self.velocity += self.acceleration + g

        velocity = self.velocity * delta_time

        if self.target_position is not None:
            self.position = vector2_move_toward(
                self.position, self.target_position, self.speed * delta_time
            )

        if self.position == self.target_position:
            self.target_position = None

        collisions = self.move(velocity, collision_rects)

        # Apply gravity?
        if g.y < 0 and collisions["bottom"]:
            self.velocity.y = 0
        if g.y > 0 and collisions["top"]:
            self.velocity.y = 0
        if g.x > 0 and collisions["right"]:
            self.velocity.x = 0
        if g.x < 0 and collisions["left"]:
            self.velocity.x = 0
