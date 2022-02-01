"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .scene import Scene

from pygame import gfxdraw
import pygame
import math
import random


class LightRoom:
    def __init__(self, scene: Scene):
        self._screen = scene.screen.copy().convert_alpha()
        self._screen.fill((0, 0, 0))

    @property
    def screen(self) -> pygame.Surface:
        self._screen.set_colorkey((0, 255, 0))
        return self._screen

    def reset(self) -> None:
        self._screen.fill((0, 0, 0))

    def draw_spot_light(
        self,
        position: pygame.Vector2,
        length: int,
        direction: int,
        spread: int,
        noise: int = 0,
    ) -> None:
        """Draws a spotlight.

        Parameters:
            position: Position of the spotlight.
            length: Length of the spotlight.
            direction: Direction of the spotlight in degrees.
            spread: Angle width of the spotlight in degrees.

        """
        points = [position]

        for n in range(int(direction - spread / 2), int(spread / 2 + direction)):
            rand_x = 0
            rand_y = 0
            if noise != 0:
                rand_x = random.randint(-noise, noise)
                rand_y = random.randint(-noise, noise)
            point = pygame.Vector2(
                int((length + rand_x) * math.cos(n * math.pi / 180)),
                int((length + rand_y) * math.sin(n * math.pi / 180)),
            )
            points.append(position + point)

        pygame.draw.polygon(self._screen, (0, 255, 0), points)

    def draw_point_light(
        self, position: pygame.Vector2, radius: int, noise: int = 0
    ) -> None:
        self.draw_spot_light(position, radius, 0, 360, noise=noise)
