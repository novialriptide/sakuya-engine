import pygame
import copy
from Sakuya.object import *
from Sakuya.math import *
from Sakuya.config import *

class Entity(Object):
    def __init__(self, position: Vector, hitbox_radius: int, surface: pygame.Surface, name = None, has_rigidbody = True, has_box_collider = True):
        super().__init__(position, hitbox_radius, name=name, has_rigidbody=has_rigidbody, has_box_collider=has_box_collider)
        self.current_frame = 0
        self.current_animation = 0
        self.animations = []
        self.surface_offset = Vector(0, 0)
        self._surface = surface

    @property
    def surface(self):
        """
        Returns a surface with the width and height in units
        """
        return pygame.transform.scale(self._surface, [to_pixels(self._surface.get_width()), to_pixels(self._surface.get_height())])
    
    def shoot(self, offset: Vector, projectile, angle: float, speed: Unit):
        """
        :param entity projectile
        :param float angle (radian)
        :param unit speed
        """
        projectile = copy.copy(projectile)
        projectile.velocity = Vector(speed * math.cos(angle), speed * math.sin(angle))
        projectile.position = self.position + offset
        return projectile

    def update(self, delta_time: float):
        super().update(delta_time)
        self.current_frame += 1