import pygame
from Sakuya.vector import *

class object:
    def __init__(self, position: vector, hitbox_radius: int, has_rigidbody: bool = True, has_box_collider: bool = True):
        self.has_rigidbody = has_rigidbody
        self.has_box_collider = has_box_collider
        self.hitbox_radius = hitbox_radius

        self.position = position
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
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
        return pygame.Rect(self.position.x - self.hitbox_radius/2, self.position.y - self.hitbox_radius/2, self.hitbox_radius, self.hitbox_radius)

    def is_collided(self, other) -> bool:
        return self.hitbox.colliderect(other.hitbox)

    def update(self, delta_time: float):
        if self._enable_on_destroy and self._on_destroy_val <= pygame.time.get_ticks():
            self._is_destroyed = True

        if self.has_rigidbody:
            self.velocity += (self.acceleration + self._gravity) * delta_time
            self.position += self.velocity * delta_time