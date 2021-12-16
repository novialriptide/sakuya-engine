from copy import copy

import pygame
import random

class Camera:
    def __init__(self, position = pygame.Vector2(0, 0), scroll = pygame.Vector2(0, 0)) -> None:
        self.position = position
        self._position = pygame.Vector2(position)
        self.scroll = scroll

        self.shake_until = pygame.time.get_ticks()
        self.shaking = False
        self.shaking_range = 0

    def shake(self, duration: int, range: float) -> None:
        """Shakes the camera

        Parameters:
            duration: How long the camera will shake in milliseconds.

        """
        if not self.shaking:
            self.shaking = True
            current_ticks = pygame.time.get_ticks()
            self.shake_until = current_ticks + duration
            self.shaking_range = range

    def update(self, delta_time: float) -> None:
        self.position += self.scroll * delta_time
        self._position += self.scroll * delta_time
        current_ticks = pygame.time.get_ticks()
        if self.shaking:
            shake_vector = pygame.Vector2(
                random.uniform(-self.shaking_range, self.shaking_range),
                random.uniform(-self.shaking_range, self.shaking_range)
            )
            self.position += shake_vector

        if self.shaking and current_ticks >= self.shake_until:
            self.shaking = False
            self.position = pygame.Vector2(self._position)
