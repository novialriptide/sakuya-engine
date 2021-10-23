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

        self._on_destroy = 0
        self._enable_on_destroy = False

    @property
    def on_destroy(self):
        return self._on_destroy
        
    def on_destroy(self, time: float):
        self._enable_on_destroy = True
        self._on_destroy = time

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.position.x - self.hitbox_radius/2, self.position.y - self.hitbox_radius/2, self.hitbox_radius, self.hitbox_radius)

    def is_collided(self, other) -> bool:
        return self.get_hitbox().colliderect(other.get_hitbox())

    def update(self, delta_time: float):
        if self._enable_on_destroy and self._on_destroy > 0:
            self.on_destroy -= delta_time
        if self._enable_on_destroy and self._on_destroy <= 0:
            del self

        if self.has_rigidbody:
            self.velocity += self.acceleration * delta_time
            self.position += self.velocity * delta_time