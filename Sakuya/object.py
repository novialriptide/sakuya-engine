import pygame
from Sakuya.vector import *

class object:
    def __init__(self, position: vector, has_rigidbody = True, has_box_collider = True):
        self.has_rigidbody = has_rigidbody
        self.has_box_collider = has_box_collider
        self.position = position
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity