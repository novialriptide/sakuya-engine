import typing
import pygame
from Sakuya.object import *
from Sakuya.vector import *

def world_to_pygame_vector(point: vector, surface_height: int):
    return vector(point.x, surface_height - point.y)

def world_to_pygame_rect(rect: pygame.Rect, surface_height: int):
    return pygame.Rect(rect.x, surface_height - rect.y, rect.width, rect.height)

class world:
    def __init__(self):
        self.objects = []
        self.gravity = vector(0, -10)
        self.current_tick = 1
        self.tps = 16

    def advance_frame(self, delta_time: float):
        """
        Updates the entities inside the world, such as physics & animation
        Should be added to the end of the main loop
        """
        if self.current_tick <= self.tps:
            self.current_tick = int(pygame.time.get_ticks() / 1000 * self.tps) % self.tps + 1
        if self.current_tick > self.tps:
            self.current_tick = 1

        for object in self.objects[:]:
            object._gravity = self.gravity
            object.update(delta_time)

            if object._is_destroyed:
                self.objects.remove(object)