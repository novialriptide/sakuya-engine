from copy import copy
from .math import vector2_move_toward

import pygame
import random

class Camera:
    def __init__(self, position = pygame.Vector2(0, 0), scroll = pygame.Vector2(0, 0)) -> None:
        self.position = position
        self._position = position.copy()
        self.move_to_position = position.copy()
        self.scroll = scroll

        self.shake_until = pygame.time.get_ticks()
        self.shaking = False
        self.shaking_range = 0

    def shake(self, duration: int, range: float, shake_speed: int = 5) -> None:
        """Shakes the camera

        Parameters:
            duration: How long the camera will shake in milliseconds.

        """
        if not self.shaking:
            self.shaking = True
            current_ticks = pygame.time.get_ticks()
            self.shake_until = current_ticks + duration
            self.shaking_range = range
            self.shake_speed = shake_speed

    def update(self, delta_time: float) -> None:
        self.position += self.scroll * delta_time
        self._position += self.scroll * delta_time
        current_ticks = pygame.time.get_ticks()
        if self.shaking:
            shake_vector = pygame.Vector2(
                random.uniform(-self.shaking_range, self.shaking_range),
                random.uniform(-self.shaking_range, self.shaking_range)
            )
            self.move_to_position = self._position + shake_vector

        if self.shaking and current_ticks >= self.shake_until:
            self.shaking = False
            self.move_to_position = self._position
        
        self.position = vector2_move_toward(self.position, self.move_to_position, self.shake_speed)