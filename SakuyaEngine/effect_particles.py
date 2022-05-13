"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import Tuple, List, TypeVar, Callable

import random
import pygame

from .physics import gravity
from .effects import BaseEffect

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)

__all__ = ["Particle", "Particles"]


class Particle(BaseEffect):
    def __init__(
        self,
        position: pygame_vector2,
        color: Tuple[int, int, int],
        velocity: pygame_vector2,
        destroy_time: int,
        obey_gravity: bool = False,
    ) -> None:

        self.position = position
        self.color = color
        self.velocity = velocity
        self.obey_gravity = obey_gravity

        self._enable_destroy = True
        self._destroy_val = destroy_time
        self._destroy_queue = False

    def draw(
        self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)
    ) -> None:
        for p in self.particles:
            surface.set_at(
                (int(p.position.x + offset.x), int(p.position.y + offset.y)), p.color
            )

    def update(self, delta_time: float, current_time: int) -> None:
        if self._enable_destroy and self._destroy_val <= current_time:
            self._destroy_queue = True

        if self.obey_gravity:
            self.velocity += gravity
        self.position += self.velocity * delta_time


class Particles:
    def __init__(
        self,
        velocity: pygame_vector2,
        spread: int = 3,
        particles_num: int = 2,
        lifetime: int = 1000,
        colors: List[Tuple[int, int, int]] = [],
        offset: pygame_vector2 = pygame.Vector2(0, 0),
        position: pygame_vector2 = pygame.Vector2(0, 0),
        obey_gravity: bool = False,
    ) -> None:
        self.particles = []
        self.velocity = velocity
        self.colors = colors
        self.spread = spread
        self.particles_num = particles_num
        self.lifetime = lifetime
        self.offset = offset
        self.position = position
        self.obey_gravity = obey_gravity

    def render(
        self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)
    ) -> None:
        for p in self.particles:
            surface.set_at(
                (int(p.position.x + offset.x), int(p.position.y + offset.y)), p.color
            )

    def update(self, delta_time: float) -> None:
        current_time = pygame.time.get_ticks()

        for p in self.particles:
            if p._destroy_queue:
                self.particles.remove(p)
            p.update(delta_time, current_time)

        destroy_time = self.lifetime + current_time
        for p in range(self.particles_num):
            random_color = random.choice(self.colors)
            random_spread_x = random.uniform(-self.spread, self.spread)
            random_spread_y = random.uniform(-self.spread, self.spread)
            par = Particle(
                self.position + self.offset,
                random_color,
                pygame.Vector2(
                    self.velocity.x + random_spread_x, self.velocity.y + random_spread_y
                ),
                destroy_time,
                obey_gravity=self.obey_gravity,
            )
            self.particles.append(par)


def load_particles_dict(data: dict) -> Particles:
    velocity = pygame.Vector2(data["velocity"])
    del data["velocity"]

    if "offset" in data.keys():
        data["offset"] = pygame.Vector2(data["offset"])

    if "position" in data.keys():
        data["position"] = pygame.Vector2(data["position"])

    return Particles(velocity, **data)
