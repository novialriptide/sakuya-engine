import pygame

from typing import Tuple

from .errors import NotImplementedError
from .math import Vector

def spotlight(surface: pygame.Surface, position: Vector, color: Tuple[int, int, int], radius: int):
    circle_surf = pygame.Surface((radius*2, radius*2))
    pygame.draw.circle(circle_surf, color, (radius, radius), radius)
    circle_surf.set_colorkey((0, 0, 0))
    position -= Vector(radius, radius)
    surface.blit(circle_surf, position.to_list(), special_flags = pygame.BLEND_RGB_ADD)

def pointlight(surface: pygame.Surface, position: Vector, distance: int):
    raise NotImplementedError