"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import TypeVar, Callable, Tuple

from .effects import BaseEffect

import pygame

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)
pygame_surface = TypeVar("pygame_surface", Callable, pygame.Surface)

__all__ = ["EnlargingCircle"]


class EnlargingCircle(BaseEffect):
    def __init__(
        self,
        position: pygame_vector2,
        color: Tuple[int, int, int],
        width: int,
        max_radius: int,
        speed: float,
    ) -> None:
        self.position = position
        self.color = color
        self.radius = 0
        self.width = width
        self.starting_width = width
        self.max_radius = max_radius
        self.speed = speed

        self._destroy_queue = False

    def draw(
        self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)
    ) -> None:
        pygame.draw.circle(
            surface, self.color, self.position + offset, self.radius, int(self.width)
        )

    def update(self, delta_time: float) -> None:
        self.radius += self.speed * delta_time
        self.width = self.starting_width * (1 - self.radius / self.max_radius) + 1

        if self.radius >= self.max_radius:
            self._destroy_queue = True
