"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from random import randint
from typing import TypeVar, Callable, List
from copy import copy

from .effects import BaseEffect

import pygame

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)
pygame_surface = TypeVar("pygame_surface", Callable, pygame.Surface)

__all__ = ["RainDrop", "Rain"]


class RainDrop(BaseEffect):
    def __init__(
        self,
        position: pygame_vector2,
        velocity: pygame_vector2,
        length: int = 5,
        color: List[int] = [255, 255, 255],
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.velocity_norm = self.velocity.normalize()
        self.length = length
        self.color = []
        for c in range(len(color)):
            self.color.append(max(min(color[c] + randint(-15, 15), 255), 0))

        self._destroy_queue = False

    def draw(
        self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)
    ) -> None:
        pos2 = self.position + self.velocity_norm * self.length
        pygame.draw.line(surface, self.color, self.position + offset, pos2 + offset)

        if (
            self.position.y < 0
            or self.position.y > surface.get_height()
            or self.position.x < 0
            or self.position.x > surface.get_width()
        ):
            self._destroy_queue = True

    def update(self, delta_time: float) -> None:
        velocity = self.velocity * delta_time
        self.position += velocity


class Rain:
    def __init__(
        self,
        drop_count: int,
        surface: pygame_surface,
        effects_list: List[RainDrop] = [],
        position: pygame_vector2 = pygame.Vector2(0, 0),
        velocity: pygame_vector2 = pygame.Vector2(2, 2),
        length: int = 5,
        color: List[int] = [255, 255, 255],
    ) -> None:
        self.drop_count = drop_count
        self.raindrops = []
        self.effects_list = effects_list
        self.position = position
        self.raindrop_velocity = velocity
        self.raindrop_length = length
        self.raindrop_color = color
        self.surface = surface
        self.surface_width = surface.get_width()
        self.surface_height = surface.get_height()

    def draw(
        self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)
    ) -> None:
        for rd in self.raindrops:
            rd.draw(surface, offset)

    def update(self, delta_time: float) -> None:
        if randint(0, 1) == 1:
            offset = pygame.Vector2(randint(0, self.surface_width), 0)
        else:
            offset = pygame.Vector2(0, randint(0, self.surface_height))

        pos = self.position + offset
        r = RainDrop(
            pos,
            self.raindrop_velocity,
            length=copy(self.raindrop_length),
            color=copy(self.raindrop_color),
        )
        self.effects_list.append(r)
