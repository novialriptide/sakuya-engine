"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from random import randint
from typing import TypeVar, Callable, Tuple, List

import pygame
import math

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)
pygame_surface = TypeVar("pygame_surface", Callable, pygame.Surface)

class BaseEffect:
    def __init__(self) -> None:
        pass
    
    def draw(self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)) -> None:
        pass
    
    def update(self, delta_time: float) -> None:
        pass

class EnlargingCircle(BaseEffect):
    def __init__(self, position: pygame_vector2, color: Tuple[int, int, int], width: int, max_radius: int, speed: float) -> None:
        self.position = position
        self.color = color
        self.radius = 0
        self.width = width
        self.starting_width = width
        self.max_radius = max_radius
        self.speed = speed

        self._destroy_queue = False

    def draw(self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)) -> None:
        pygame.draw.circle(surface, self.color, self.position + offset, self.radius, int(self.width))

    def update(self, delta_time: float) -> None:
        self.radius += self.speed * delta_time
        self.width = self.starting_width * (1 - self.radius / self.max_radius) + 1

        if self.radius >= self.max_radius:
            self._destroy_queue = True

class RainDrop(BaseEffect):
    def __init__(
        self,
        position: pygame_vector2,
        velocity: pygame_vector2,
        length: int = 5,
        color: Tuple[int, int, int] = (255, 255, 255),
        destroy_time = 2000
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.length = length
        self.color = color

        self._enable_destroy = True
        self._destroy_val = destroy_time + pygame.time.get_ticks()
        self._destroy_queue = False

    def destroy(self, time: int) -> None:
        """Set the destruction time.

        Parameters:
            time: milliseconds to destruction

        """
        self._enable_destroy = True
        self._destroy_val = time + pygame.time.get_ticks()

    def draw(self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)) -> None:
        pos2 = self.position + self.velocity.normalize() * self.length
        pygame.draw.line(surface, self.color, self.position + offset, pos2 + offset)

    def update(self, delta_time: float) -> None:
        current_time = pygame.time.get_ticks()
        if self._enable_destroy and self._destroy_val <= current_time:
            self._destroy_queue = True
        self.position += self.velocity * delta_time

class Rain:
    def __init__(
        self,
        drop_count: int,
        surface: pygame_surface,
        effects_list: List[RainDrop] = [],
        position: pygame_vector2 = pygame.Vector2(0, 0),
        velocity: pygame_vector2 = pygame.Vector2(2, 2),
        length: int = 5,
        color: Tuple[int, int, int] = (255, 255, 255),
        destroy_time: int = 2000,
    ) -> None:
        self.drop_count = drop_count
        self.raindrops = []
        self.effects_list = effects_list
        self.position = position
        self.raindrop_velocity = velocity
        self.raindrop_length = length
        self.raindrop_color = color
        self.raindrop_destroy_time = destroy_time
        self.surface = surface
        self.surface_width = surface.get_width()
        self.surface_height = surface.get_height()

    def draw(self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)) -> None:
        for rd in self.raindrops:
            rd.draw(surface, offset)

    def update(self, delta_time: float) -> None:
        if randint(0, 1) == 1:
            offset = pygame.Vector2(randint(0, self.surface_width), 0)
        else:
            offset = pygame.Vector2(0, randint(0, self.surface_height))

        pos = self.position + offset
        for d in range(self.drop_count):
            r = RainDrop(
                pos,
                self.raindrop_velocity,
                length = self.raindrop_length,
                color = self.raindrop_color,
                destroy_time = self.raindrop_destroy_time
            )
            self.effects_list.append(r)
        for rd in self.raindrops:
            rd.update(delta_time)
