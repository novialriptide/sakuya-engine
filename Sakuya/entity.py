import pygame
from Sakuya.vector import *
from Sakuya.object import *

class entity(object):
    def __init__(self, position: vector, hitbox_radius: int, has_rigidbody = True, has_box_collider = True):
        super().__init__(position, hitbox_radius, has_rigidbody=has_rigidbody, has_box_collider=has_box_collider)
        self.current_frame = 0
        self.current_animation = 0
        self.animations = []
        self.sprite_offset = vector(0, 0)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.current_frame += 1