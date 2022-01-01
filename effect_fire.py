"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List, TypeVar, Callable, Tuple
from Helix.SakuyaEngine.effect_particles import Particle, Particles

import pygame

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)

"""
This fire particle will become bigger, go from colors yellow to orange to red, and become transparent over its lifetime

Fire can also be applied to Entities since its a child class of Particles
"""

class FireParticle(Particle):
    def __init__(
        self,
        position: pygame_vector2,
        color: Tuple[int, int, int],
        velocity: pygame_vector2,
        destroy_time: int
    ) -> None:
        super().__init__(position, color, velocity, destroy_time)

class Fire(Particles):
    def __init__(
        self,
        velocity: pygame_vector2,
        color_palette: List[Tuple[int, int, int]],
        spread: int = 3,
        particles_num: int = 2,
        lifetime: int = 1000,
        offset: pygame_vector2 = pygame.Vector2(0, 0),
        position: pygame_vector2 = pygame.Vector2(0, 0)
    ) -> None:
        super().__init__(
            velocity,
            spread = spread,
            particles_num = particles_num,
            lifetime = lifetime,
            offset = offset,
            position = position
        )
        self.color_palette = color_palette