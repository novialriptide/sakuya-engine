from typing import Generic, Literal, Tuple, List, Union

from .scene import Scene
from .math import get_angle
from .draw import draw_pie
from .locals import HINDERED_VISION_MODE, UNHINDERED_VISION_MODE

import math
import copy
import pygame


class LightRoom:
    def __init__(
        self,
        scene: Scene,
        force_size: Union[None, Tuple[int, int]] = None,
        shadow_color: Tuple[int, int, int] = (0, 0, 0),
        mode: Generic[
            HINDERED_VISION_MODE, UNHINDERED_VISION_MODE
        ] = HINDERED_VISION_MODE,
        alpha: int = 1,
    ) -> None:
        self.shadow_color = shadow_color
        self._scene = scene

        if force_size is None:
            self._surface = scene.screen.copy().convert_alpha()
        else:
            self._surface = pygame.Surface(force_size).convert_alpha()

        self.mode = mode
        self.alpha = alpha

        self._surface.fill(self.shadow_color)
        self._light_surfs = []
        self._base_light_color = (0, 255, 0)
        self._crop_color = (255, 0, 0)

    @property
    def scene(self) -> Scene:
        return self._scene

    @property
    def surface(self) -> pygame.Surface:
        if self.mode is HINDERED_VISION_MODE:
            self._surface.fill(self.shadow_color)

        for s in self._light_surfs:
            self._surface.blit(s["crop_surf"], (0, 0))

        surf_array = pygame.PixelArray(self._surface)
        surf_array.replace(self._base_light_color, (0, 0, 255, 0))
        surf_array.close()

        for s in self._light_surfs:
            self._surface.blit(s["color_surf"], (0, 0))
        self._light_surfs = []

        return self._surface

    def _draw_shadows(
        self,
        surface: pygame.Surface,
        origin_position: pygame.Vector2,
        length: int,
        collisions: List[Tuple[int, int]] = [],
    ) -> None:
        shadow_points = []
        for line in collisions:
            points = list(copy.copy(line))

            angle1 = get_angle(origin_position, line[1])
            point1 = pygame.Vector2(math.cos(angle1), math.sin(angle1))
            point1 *= length * 2

            points.append(pygame.Vector2(line[1]) + point1)

            angle2 = get_angle(origin_position, line[0])
            point2 = pygame.Vector2(math.cos(angle2), math.sin(angle2))
            point2 *= length * 2
            points.append(pygame.Vector2(line[0]) + point2)

            shadow_points.append(points)

        for p in shadow_points:
            pygame.draw.polygon(surface, self._crop_color, p)

    def draw_spot_light(
        self,
        position: pygame.Vector2,
        length: int,
        direction: int,
        spread: int,
        collisions: List[Tuple[int, int]] = [],
        color: Tuple[int, int, int, int] = (255, 255, 255, 25),
    ) -> None:
        start_angle = int(direction - spread / 2)
        end_angle = int(direction + spread / 2)
        light_pos = position

        color_surf = self._surface.copy().convert_alpha()
        color_surf.fill((0, 0, 0, 0))
        draw_pie(
            color_surf,
            self._base_light_color,
            light_pos,
            length,
            start_angle,
            end_angle,
        )
        self._draw_shadows(color_surf, light_pos, length, collisions=collisions)

        surf_array = pygame.PixelArray(color_surf)
        surf_array.replace(self._crop_color, (0, 0, 0, 0))

        crop_surf = color_surf.copy()

        surf_array.replace(self._base_light_color, color)
        surf_array.close()

        self._light_surfs.append({"color_surf": color_surf, "crop_surf": crop_surf})

    def draw_point_light(
        self,
        position: pygame.Vector2,
        radius: int,
        collisions: List[Tuple[int, int]] = [],
        color: Tuple[int, int, int, int] = (255, 255, 255, 25),
    ) -> None:
        self.draw_spot_light(
            position, radius, 0, 360, collisions=collisions, color=color
        )

    def draw_area_light(
        self,
        position1: pygame.Vector2,
        position2: pygame.Vector2,
        length: int,
        direction: float,
        color: Tuple[int, int, int, int] = (255, 255, 255, 25),
    ):
        pass
