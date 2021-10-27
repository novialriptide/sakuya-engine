import typing
import pygame
from Sakuya.object import *
from Sakuya.math import *
from Sakuya.config import *

class World:
    def __init__(self):
        self.objects = []
        self.gravity = Vector(0, 10)
        self.current_tick = 1
        self.time_elapsed = 0

    def test_collisions(self, object: Object):
        objects = self.objects[:]
        objects.remove(object)
        collided = []
        for o in objects:
            if object.hitbox.collidecircle(o.hitbox):
                collided.append(o)

        return collided

    def advance_frame(self, delta_time: float):
        """
        Updates the entities inside the world, such as physics & animation
        Should be added to the end of the main loop
        """
        if self.current_tick <= TICKS_PER_SECOND:
            self.current_tick = int(pygame.time.get_ticks() / 1000 * TICKS_PER_SECOND) % TICKS_PER_SECOND + 1
        if self.current_tick > TICKS_PER_SECOND:
            self.current_tick = 1
            self.time_elapsed += 1

        for object in self.objects[:]:
            object._gravity = self.gravity
            object.update(delta_time)

            if object._is_destroyed:
                self.objects.remove(object)