"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List, Tuple
import pygame
from math import *

class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        methods: List[dict] = [{"func": None, "args": [], "kwargs": {}}, ...],
        color: Tuple[int, int, int] = (255, 255, 255),
        key: pygame.key or None = None
    ) -> None:
        self.rect = rect
        self.key = key
        self.methods = methods
        self.color = color
        
        self._pressed_up_times = 0
        self._pressed_down_times = 0

    @property
    def is_pressing_key(self) -> bool:
        if self.key is not None:
            return pygame.key.get_pressed()[self.key] == 1
        else:
            return False

    def is_pressing_mousedown(self, point: pygame.Vector2) -> bool:
        return (pygame.mouse.get_pressed()[0] or self.is_pressing_key) and self.is_hovering(point)

    def is_pressing_mouseup(self, point: pygame.Vector2) -> bool:
        return (pygame.mouse.get_pressed()[1] or self.is_pressing_key) and self.is_hovering(point)

    def is_pressing_mousedown_instant(self, point: pygame.Vector2) -> bool:
        eval = self.is_pressing_mousedown(point)

        if not eval:
            self._pressed_down_times = 0

        if eval:
            self._pressed_down_times += 1

        if self._pressed_down_times > 1 and eval:
            return False

        return eval

    def is_pressing_mouseup_instant(self, point: pygame.Vector2) -> bool:
        eval = self.is_pressing_mouseup(point)

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
