"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from __future__ import annotations
from typing import List
from copy import copy

import pygame
import math

from .animation import Animation

__all__ = ["Entity"]


class Entity:
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: float = 1,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        obey_gravity: bool = False,
        speed: float = 0,
        custom_hitbox_size: pygame.Vector2 = pygame.Vector2(0, 0),
        gravity_scale: float = 1,
        static_sprite: pygame.Surface = None,
        ignore_collisions: bool = False,
    ):
        self.name = name
        self.tags = tags
        self.scale = pygame.Vector2(1, 1) * scale
        self._clock = None

        # Collisions & Physics
        self.position = position
        self.obey_gravity = obey_gravity
        self.custom_hitbox_size = custom_hitbox_size
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._custom_hitbox_rect = pygame.Rect(0, 0, 0, 0)
        self.gravity_scale = gravity_scale
        self.gravity = pygame.Vector2(1, 0)
        self.ignore_collisions = ignore_collisions

        # Animations
        self.animations = {}
        self.current_anim = None
        self.static_sprite = static_sprite

        # Destroy
        self._destroy_val = 0
        self._enable_destroy = False
        self._destroy_queue = False

        # Rotations & Static Objects
        self._static_rect = pygame.Rect(0, 0, 0, 0)
        self._sprite = None
        self.direction = 0
        self.angle = 0
        self.rotation_offset = pygame.Vector2(0, 0)
        self.alpha = 255

    @property
    def sprite(self) -> pygame.Surface:
        out_sprite = None
        sprite = self.anim_get(self.current_anim).sprite
        if self.scale.x != 1 or self.scale.y != 1:
            width, height = self._sprite.get_size()
            scaled_sprite = pygame.transform.scale(
                sprite, (self.scale.x * width, self.scale.y * height)
            )
            out_sprite = scaled_sprite
        else:
            out_sprite = sprite

        # Rotate sprite
        direction = -self.angle + 360
        if self.direction != direction:
            self._sprite = pygame.transform.rotate(out_sprite, direction)
            rect_width, rect_height = self.static_rect.size
            sprite_width, sprite_height = self._sprite.get_size()
            self.rotation_offset.x = rect_width / 2 - sprite_width / 2
            self.rotation_offset.y = rect_height / 2 - sprite_height / 2
            self.direction = direction

        self._sprite.set_alpha(self.alpha)
        return self._sprite

    @sprite.setter
    def sprite(self, value: pygame.Surface) -> None:
        self._sprite = value

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
        self._rect.x += self.rotation_offset.x
        self._rect.y += self.rotation_offset.y
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
    def static_rect(self) -> pygame.Rect:
        curr_anim = self.anim_get(self.current_anim)
        if self.static_sprite is not None:
            width, height = self.static_sprite.get_size()
            self._static_rect.x = self.position.x
            self._static_rect.y = self.position.y
            self._static_rect.width = width
            self._static_rect.height = height
        elif curr_anim is not None:
            width, height = curr_anim.sprite.get_size()
            self._static_rect.x = self.position.x
            self._static_rect.y = self.position.y
            self._static_rect.width = width
            self._static_rect.height = height

        return self._static_rect

    @property
    def center_offset(self) -> pygame.Vector2:
        s = self.sprite
        if s is not None:
            width, height = s.get_size()
        else:
            r = self.rect
            width, height = r.width, r.height
        return pygame.Vector2(width / 2, height / 2) + self.rotation_offset

    @property
    def center_position(self) -> pygame.Vector2:
        return self.position + self.center_offset

    def destroy(self, time: int) -> None:
        """Set the destruction time.

        Parameters:
            time: milliseconds to destruction

        """
        self._enable_destroy = True
        self._destroy_val = time + self._clock.get_time()

    @property
    def abs_position(self) -> pygame.Vector2:
        return self.position + self.rotation_offset

    @property
    def abs_center_position(self) -> pygame.Vector2:
        return self.position + self.rotation_offset + self.center_offset

    def move(
        self, movement: pygame.Vector2, collision_rects: List[pygame.Rect]
    ) -> bool:
        def special_round(val: float) -> int:
            if val > 0:
                return math.ceil(val)
            elif val < 0:
                return math.floor(val)
            elif val == 0:
                return 0

        hit = {"top": False, "bottom": False, "left": False, "right": False}
        test_rect = self.static_rect.copy()
        self.position.x += movement.x
        test_rect.x += special_round(movement.x)
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)

        for c in verified_collisions:
            if movement.x > 0:
                test_rect.right = c.left
                hit["right"] = True
                self.on_col_right()
            elif movement.x < 0:
                test_rect.left = c.right
                hit["left"] = True
                self.on_col_left()

            self.position.x = test_rect.x

        self.position.y += movement.y
        test_rect.y += special_round(movement.y)
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)
        for c in verified_collisions:
            if movement.y > 0:
                test_rect.bottom = c.top
                hit["bottom"] = True
                self.on_col_bottom()
            elif movement.y < 0:
                test_rect.top = c.bottom
                hit["top"] = True
                self.on_col_top()

            self.position.y = test_rect.y

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

    def advance_frame(
        self, delta_time: float, collision_rects: List[pygame.Rect] = []
    ) -> None:
        # Destroy
        if self._enable_destroy and self._destroy_val <= self._clock.get_time():
            self._destroy_queue = True

        # Update Animation
        if self.current_anim is not None:
            self.anim_get(self.current_anim).update(delta_time)

        g = self.gravity
        if not self.obey_gravity:
            g = pygame.Vector2(0, 0)

        # Apply velocity
        self.velocity += self.acceleration + g

        velocity = self.velocity * delta_time

        if self.ignore_collisions:
            collision_rects = []

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

    def on_col_top(self) -> None:
        pass

    def on_col_bottom(self) -> None:
        pass

    def on_col_right(self) -> None:
        pass

    def on_col_left(self) -> None:
        pass

    def on_awake(self, scene) -> None:
        pass

    def on_destroy(self, scene) -> None:
        pass

    def on_update(self, scene) -> None:
        pass
