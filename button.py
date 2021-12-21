"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from typing import List
import pygame
from math import *

class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        methods: List[dict] = [],
        key: bool = None
    ) -> None:
        self.rect = rect
        self.key = key
        self.methods = methods
        
        self._pressed_up_times = 0
        self._pressed_down_times = 0

    @property
    def is_pressing_key(self) -> bool:
        return pygame.key.get_pressed()[self.key] == 1

    def is_pressing_mousedown(self, point: pygame.Vector2) -> bool:
        return pygame.mouse.get_pressed()[0] and self.is_hovering(point)

    def is_pressing_mouseup(self, point: pygame.Vector2) -> bool:
        return pygame.mouse.get_pressed()[1] and self.is_hovering(point)

    def is_pressing_mousedown_instant(self, point: pygame.Vector2) -> bool:
        eval = pygame.mouse.get_pressed()[0] and self.is_hovering(point)

        if not eval:
            self._pressed_down_times = 0

        if eval:
            self._pressed_down_times += 1

        if self._pressed_down_times > 1 and eval:
            return False

        return eval

    def is_pressing_mouseup_instant(self, point: pygame.Vector2) -> bool:
        eval = pygame.mouse.get_pressed()[1] and self.is_hovering(point)

        if not eval:
            self._pressed_up_times = 0

        if eval:
            self._pressed_up_times += 1

        if self._pressed_up_times > 1 and eval:
            return False
        
        return eval

    def is_hovering(self, point: pygame.Vector2) -> bool:
        return self.rect.collidepoint(point)

    def execute(self) -> None:
        for f in self.methods: f["func"](*f["args"], **f["kwargs"])
