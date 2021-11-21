import pygame
from Sakuya.math import *
from Sakuya.circle import *
from Sakuya.config import *

class Object:
    def __init__(self, position: Vector, hitbox_radius: Unit, name = None, has_rigidbody: bool = True, has_box_collider: bool = True):
        """
        :param vector(unit, unit) position
        :param unit hitbox_radius
        :param bool has_rigidbody
        :param bool has_box_collider
        """
        self.name = name
        self.has_rigidbody = has_rigidbody
        self.has_box_collider = has_box_collider
        self.hitbox_radius = hitbox_radius

        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self._gravity = None

        self._on_destroy_val = 0
        self._enable_on_destroy = False
        self._is_destroyed = False
        
    def on_destroy(self, time: int):
        """
        :param int time: milliseconds to destruction
        """
        self._enable_on_destroy = True
        self._on_destroy_val = time + pygame.time.get_ticks()

    @property
    def hitbox(self) -> pygame.Rect:
        hitbox_radius_pixels = to_pixels(self.hitbox_radius)
        position_pixels = to_pixels(self.position)
        return pygame.Rect(position_pixels.x - hitbox_radius_pixels, position_pixels.y - hitbox_radius_pixels, hitbox_radius_pixels*2, hitbox_radius_pixels*2)

    def is_collided(self, other) -> bool:
        return self.hitbox.colliderect(other.hitbox)

    def move_to(self, movement: Vector, collisions):
        test_rect = self.hitbox
        test_rect.x += to_pixels(movement.x)
        test_rect.y += to_pixels(movement.y)

        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        hit_collisions = []

        for c in collisions:
            if self.is_collided(c):
                hit_collisions.append(c)

        if self.has_box_collider:
            for h in hit_collisions:
                if to_pixels(movement.x) > 0:
                    pass

    def update(self, delta_time: float):
        if self._enable_on_destroy and self._on_destroy_val <= pygame.time.get_ticks():
            self._is_destroyed = True

        if self.has_rigidbody:
            self.velocity += (self.acceleration + self._gravity) * delta_time
            self.position += self.velocity * delta_time