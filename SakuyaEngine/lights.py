"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .scene import Scene

from pygame import gfxdraw
import pygame

class LightRoom:
    def __init__(self, scene: Scene):
        self._screen = scene.screen.copy().convert_alpha()
        self._screen.fill((0, 0, 0))
    
    @property
    def screen(self) -> pygame.Surface:
        self._screen.set_colorkey((0, 255, 0))
        return self._screen
    
    def add_point_light(self, position: pygame.Vector2, radius: int):
        pygame.draw.circle(self._screen, (0, 255, 0), position, radius)