"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .math import raycast
from .scene import Scene

import pygame
import math
import random


class LightRoom:
    def __init__(self, scene: Scene):
        self._screen = scene.screen.copy().convert_alpha()
        self._screen.fill((0, 0, 0))

        self._outer_color = (0, 0, 100)
        self._mid_color = (0, 0, 175)
        self._inner_color = (0, 0, 255)

        self._outer_points = []
        self._inner_points = []

    @property
    def surface(self) -> pygame.Surface:
        self._screen.fill((0, 0, 0))
        for outer_points in self._outer_points:
            pygame.draw.polygon(self._screen, self._outer_color, outer_points)
        for inner_points in self._inner_points:
            pygame.draw.polygon(self._screen, self._inner_color, inner_points)

        screen_array = pygame.PixelArray(self._screen)  # lgtm [py/call/wrong-arguments]
        screen_array.replace(self._outer_color, (0, 0, 0, 50))
        screen_array.replace(self._inner_color, (0, 0, 0, 0))

        self._outer_points = []
        self._inner_points = []

        return self._screen

    def draw_spot_light(
        self,
        position: pygame.Vector2,
        length: int,
        direction: int,
        spread: int,
        noise: int = 0,
        collisions=[],
    ) -> None:
        """Draws a spotlight.

        Parameters:
            position: Position of the spotlight.
            length: Length of the spotlight.
            direction: Direction of the spotlight in degrees.
            spread: Angle width of the spotlight in degrees.

        """
        # TODO: Optimize by using this article: https://www.redblobgames.com/articles/visibility/
        
        outer_points = [position]
        inner_points = [position]

        angle1 = int(direction - spread / 2)
        angle2 = int(direction + spread / 2)
        for n in range(angle1, angle2):
            rand_x = 0
            rand_y = 0
            if noise != 0:
                rand_x = random.randint(-noise, noise)
                rand_y = random.randint(-noise, noise)

            point1 = pygame.Vector2(
                int((length + rand_x) * math.cos(n * math.pi / 180)),
                int((length + rand_y) * math.sin(n * math.pi / 180)),
            )

            outer_point = raycast(position, position + point1, collisions)

            outer_points.append(outer_point)
            point2 = pygame.Vector2(
                int((length * 0.5 + rand_x) * math.cos(n * math.pi / 180)),
                int((length * 0.5 + rand_y) * math.sin(n * math.pi / 180)),
            )

            inner_point = raycast(position, position + point2, collisions)

            inner_points.append(inner_point)

        self._outer_points.append(outer_points)
        self._inner_points.append(inner_points)

    def draw_point_light(
        self,
        position: pygame.Vector2,
        radius: int,
        noise: int = 0,
        collisions=[],
    ) -> None:
        self.draw_spot_light(
            position, radius, 0, 360, noise=noise, collisions=collisions
        )
