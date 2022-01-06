"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import TypeVar, Callable

import pygame

pygame_vector2 = TypeVar("pygame_vector2", Callable, pygame.Vector2)
pygame_surface = TypeVar("pygame_surface", Callable, pygame.Surface)

class BaseEffect:
    def __init__(self) -> None:
        pass
    
    def draw(self, surface: pygame_surface, offset: pygame_vector2 = pygame.Vector2(0, 0)) -> None:
        pass
    
    def update(self, delta_time: float) -> None:
        pass