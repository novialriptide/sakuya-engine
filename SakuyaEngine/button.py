"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List, Tuple
import pygame
from math import *

__all__ = ["Button"]


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        method: callable = lambda: None,
        rect_color: Tuple[int, int, int] = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        text: str = "",
        key: pygame.key or None = None,
    ) -> None:
        self.font = pygame.font.SysFont("Arial", rect.height)
        self.text_surf = self.font.render(text, False, text_color)
        self.rect = rect
        self.key = key
        self.method = method
        self.rect_color = rect_color

        self._is_pressed = False

    @property
    def pressed_key(self) -> bool:
        if self.key is not None:
            return pygame.key.get_pressed()[self.key] == 1
        else:
            return False

    def is_hovering(self, point: pygame.Vector2) -> bool:
        return self.rect.collidepoint(point)

    def draw(self, surface):
        """Draws the pygame.Rect and font"""
        pygame.draw.rect(surface, self.rect_color, self.rect)
        surface.blit(
            self.text_surf,
            pygame.Vector2(self.rect.center)
            - pygame.Vector2(self.text_surf.get_size()) / 2,
        )

    def execute(self) -> None:
        self.method()

    def update(self):
        """Must be called every frame."""
        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
            and not self._is_pressed
        ):
            self.execute()
            self._is_pressed = True

        elif (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and not pygame.mouse.get_pressed()[0]
            and self._is_pressed
        ):
            self._is_pressed = False
