import pygame
from Sakuya.vector import *
from Sakuya.object import *

class entity(object):
    def __init__(self, position: vector, has_rigidbody = True, has_box_collider = True):
        super().__init__(position, has_rigidbody=has_rigidbody, has_box_collider=has_box_collider)
        self.current_frame = 0
        self.current_animation = 0
        self.animations = []

    def update(self):
        super().update()
        self.current_frame += 1