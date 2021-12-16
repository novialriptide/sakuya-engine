"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from typing import Tuple, List, TypeVar, Callable

import random
import pygame

from .physics import gravity

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)

class Particle:
    def __init__(
        self,
        position: pygame_vector2,
        color: Tuple[int, int, int],
        velocity: pygame_vector2,
        destroy_time: int
    ) -> None:
        
        self.position = position
        self.color = color
        self.velocity = velocity
        
        self._enable_destroy = True
        self._destroy_val = destroy_time
        
        self._is_destroyed = False

    def update(self, delta_time: float, current_time: int) -> None:
        if self._enable_destroy and self._destroy_val <= current_time:
            self._is_destroyed = True

        self.velocity += gravity
        self.position += self.velocity * delta_time

class Particles:
    def __init__(
        self,
        velocity: pygame_vector2,
        spread: int = 3,
        particles_num: int = 2,
        colors: List[Tuple[int, int, int]] = [],
        lifetime: int = 1000,
        offset: pygame_vector2 = pygame.Vector2(0, 0),
        position: pygame_vector2 = pygame.Vector2(0, 0)
    ) -> None:
        self.particles = []
        self.velocity = velocity

        screen = pygame.display.get_surface()
        self.colors = [screen.map_rgb(col) for col in colors]
        
        #self.colors = colors
        self.spread = spread # pygame.Vector2
        self.particles_num = particles_num # int
        self.lifetime = lifetime
        self.offset = offset
        self.position = position
    
    def render(self, surface: pygame.Surface, offset: pygame.Vector2 = pygame.Vector2(0, 0)) -> None:
        for p in self.particles:
            surface.set_at((int(p.position.x + offset.x), int(p.position.y + offset.y)), p.color)

    def update(self, delta_time: float) -> None:
        current_time = pygame.time.get_ticks()

        for p in self.particles:
            if p._is_destroyed:
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
                pygame.Vector2(self.velocity.x + random_spread_x, self.velocity.y + random_spread_y),
                destroy_time
            )
            self.particles.append(par)

def load_particles_dict(data: dict) -> Particles:
    velocity = pygame.Vector2(data["velocity"])
    del data["velocity"]

    if "offset" in data.keys():
        data["offset"] = pygame.Vector2(data["offset"])

    if "position" in data.keys():
        data["position"] = pygame.Vector2(data["position"])

    return Particles(
        velocity,
        **data
    )