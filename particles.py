from .math import Vector
from .physics import gravity
from typing import Tuple, List

import random
import math
import pygame

class Particle:
    def __init__(
        self,
        position: Vector,
        color: Tuple[int, int, int],
        velocity: Vector
    ):
        self.position = position
        self.color = color
        self.velocity = velocity
        self._on_destroy_val = 0
        self._enable_on_destroy = False
        self._is_destroyed = False
        
    def on_destroy(self, time: int) -> None:
        """
        :param int time: milliseconds to destruction
        """
        self._enable_on_destroy = True
        self._on_destroy_val = time + pygame.time.get_ticks()

    def update(self, delta_time: float) -> None:
        if self._enable_on_destroy and self._on_destroy_val <= pygame.time.get_ticks():
            self._is_destroyed = True

        self.velocity += gravity
        self.position += self.velocity * math.pow(delta_time, 2)

class Particles:
    def __init__(
        self,
        velocity: Vector,
        spread: int = 3,
        particles_num: int = 2,
        colors: List[Tuple[int, int, int]] = [],
        lifetime: int = 1000,
        offset: Vector = Vector(0,0)
    ):
        self.particles = []
        self.velocity = velocity
        self.colors = colors
        self.spread = spread # Vector
        self.particles_num = particles_num # int
        self.lifetime = lifetime
        self.offset = offset
    
    def render(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            surface.set_at((int(p.position.x), int(p.position.y)), p.color)

    def update(self, delta_time: float, position: Vector) -> None:
        for p in range(self.particles_num):
            random_color = random.randrange(0, len(self.colors))
            random_spread_x = random.uniform(-self.spread, self.spread)
            random_spread_y = random.uniform(-self.spread, self.spread)
            par = Particle(
                position + self.offset,
                self.colors[random_color],
                Vector(self.velocity.x + random_spread_x, self.velocity.y + random_spread_y)
            )
            par.on_destroy(self.lifetime)
            self.particles.append(par)

        for p in self.particles:
            if p._is_destroyed:
                self.particles.remove(p)
            p.update(delta_time)