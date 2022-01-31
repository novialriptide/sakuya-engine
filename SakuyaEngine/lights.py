"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import Tuple, TypeVar, Callable

import pygame

from .errors import NotImplementedError

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)


def light(
    surface: pygame.Surface,
    position: pygame_vector2,
    color: Tuple[int, int, int],
    radius: int,
    brightness: int = 1,
):
    position -= pygame.Vector2(radius, radius)
    for d in range(brightness):
        circle_surf = pygame.Surface(
            (radius * 2, radius * 2)
        )  # lgtm [py/call/wrong-arguments]
        pygame.draw.circle(
            circle_surf, color, (radius, radius), radius * (d / brightness)
        )
        circle_surf.set_colorkey((0, 0, 0))
        surface.blit(circle_surf, position, special_flags=pygame.BLEND_RGB_ADD)


def shadow(
    surface: pygame.Surface,
    position: pygame_vector2,
    darkness: int,
    radius: int,
    offset=pygame.Vector2(0, 0),
):
    position += offset
    circle_surf = pygame.Surface(
        (radius * 2, radius * 2), pygame.SRCALPHA
    )  # lgtm [py/call/wrong-arguments]
    pygame.draw.circle(circle_surf, (0, 0, 0, darkness), (radius, radius), radius)
    position -= pygame.Vector2(radius, radius)
    surface.blit(circle_surf, position)


def pointlight(surface: pygame.Surface, position: pygame_vector2, distance: int):
    raise NotImplementedError
