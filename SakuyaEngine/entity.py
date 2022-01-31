"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from __future__ import annotations
from typing import List

import pygame

from .locals import DEFAULT_TEXTURE


class BaseEntity:
    def __init__(
        self,
        name: str = None,
        tags: List[str] = [],
        scale: float = 1,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        terminal_velocity: bool = False,
        obey_gravity: bool = False,
        speed: float = 0,
        custom_hitbox_size: pygame.Vector2 = pygame.Vector2(0, 0),
        gravity_scale: float = 1,
    ):
        self.name = name
        self.tags = tags
        self.scale = pygame.Vector2(1, 1) * scale
        self._clock = None

        # Collisions & Physics
        self.position = position
        self.obey_gravity = obey_gravity
        self.terminal_velocity = terminal_velocity
        self.custom_hitbox_size = custom_hitbox_size
        self.speed = speed
        self.terminal_velocity = 10.0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._custom_hitbox_rect = pygame.Rect(0, 0, 0, 0)
        self.gravity_scale = gravity_scale
        self.gravity = pygame.Vector2(1, 0)

        # Destroy
        self._destroy_val = 0
        self._enable_destroy = False
        self._destroy_queue = False

        # Rotations & Static Objects
        self._static_rect = pygame.Rect(0, 0, 0, 0)
        self._sprite = DEFAULT_TEXTURE
        self.direction = 0
        self.angle = 0
        self.rotation_offset = pygame.Vector2(0, 0)

    @property
    def sprite(self) -> pygame.Surface:
        out_sprite = None
        if self.scale.x != 1 or self.scale.y != 1:
            width, height = self._sprite.get_size()
            scaled_sprite = pygame.transform.scale(
                self._sprite, (self.scale.x * width, self.scale.y * height)
            )
            out_sprite = scaled_sprite
        else:
            out_sprite = self._sprite

        # Rotate sprite
        direction = -self.angle + 360
        if self.direction != direction:
            self._sprite = pygame.transform.rotate(out_sprite, direction)
            rect_width, rect_height = self.static_rect.size
            sprite_width, sprite_height = self._sprite.get_size()
            self.rotation_offset.x = rect_width / 2 - sprite_width / 2
            self.rotation_offset.y = rect_height / 2 - sprite_height / 2
            self.direction = direction

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
        hit = {"top": False, "bottom": False, "left": False, "right": False}
        self.position.x += movement.x
        test_rect = self.static_rect.copy()
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)

        for c in verified_collisions:
            if movement.x > 0:
                test_rect.right = c.left
                self.position.x = test_rect.x
                hit["right"] = True
            elif movement.x < 0:
                test_rect.left = c.right
                self.position.x = test_rect.x
                hit["left"] = True

        self.position.y += movement.y
        test_rect = self.static_rect.copy()
        verified_collisions = []
        for c in collision_rects:
            if test_rect.colliderect(c):
                verified_collisions.append(c)
        for c in verified_collisions:
            if movement.y > 0:
                test_rect.bottom = c.top
                self.position.y = test_rect.y
                hit["bottom"] = True
            elif movement.y < 0:
                test_rect.top = c.bottom
                self.position.y = test_rect.y
                hit["top"] = True

        return hit

    def advance_frame(
        self, delta_time: float, collision_rects: List[pygame.Rect] = []
    ) -> None:
        # Destroy
        if self._enable_destroy and self._destroy_val <= self._clock.get_time():
            self._destroy_queue = True

        if self.destroy_position == self.position:
            self._destroy_queue = True

        # Apply terminal velocity
        term_vec = self.terminal_velocity * delta_time
        if self.terminal_velocity:
            if self.velocity.x < 0:
                self.velocity.x = max(self.velocity.x, term_vec)
            if self.velocity.x > 0:
                self.velocity.x = min(self.velocity.x, term_vec)
            if self.velocity.y < 0:
                self.velocity.y = max(self.velocity.y, term_vec)
            if self.velocity.y > 0:
                self.velocity.y = min(self.velocity.y, term_vec)

        g = self.gravity
        if not self.obey_gravity:
            g = pygame.Vector2(0, 0)

        # Apply velocity
        self.velocity += self.acceleration + g

        velocity = self.velocity * delta_time

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

    def on_awake(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_update(self) -> None:
        pass
