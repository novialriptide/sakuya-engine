from .clock import Clock

import pygame
import random

__all__ = ["Camera"]


class Camera:
    def __init__(
        self,
        position: pygame.Vector2 = pygame.Vector2(0, 0),
        scroll: pygame.Vector2 = pygame.Vector2(0, 0),
        clock: Clock = None,
    ) -> None:
        self.position = position
        self._position = position.copy()
        self.move_to_position = position.copy()
        self.scroll = scroll

    def update(self, delta_time: float) -> None:
        self.position += self.scroll * delta_time
        self._position += self.scroll * delta_time
