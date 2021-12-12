import pygame

from typing import Tuple

from .errors import NotImplementedError

def spotlight(surface: pygame.Surface, position: pygame.math.Vector2, color: Tuple[int, int, int], radius: int):
    circle_surf = pygame.Surface((radius*2, radius*2))
    pygame.draw.circle(circle_surf, color, (radius, radius), radius)
    circle_surf.set_colorkey((0, 0, 0))
    position -= pygame.math.Vector2(radius, radius)
    surface.blit(circle_surf, position, special_flags = pygame.BLEND_RGB_ADD)

def pointlight(surface: pygame.Surface, position: pygame.math.Vector2, distance: int):
    raise NotImplementedError