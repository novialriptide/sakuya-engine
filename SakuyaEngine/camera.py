from .clock import Clock
from .math import vector2_move_toward

import pygame
import random


class Camera:
    def __init__(
        self,
        position: pygame.Vector2=pygame.Vector2(0, 0),
        scroll: pygame.Vector2=pygame.Vector2(0, 0),
        clock: Clock=None
    ) -> None:
        self.position = position
        self._position = position.copy()
        self.move_to_position = position.copy()
        self.scroll = scroll
        self.clock = clock
        
        if self.clock is None:
            self.shake_until = pygame.time.get_ticks()
        else:
            self.shake_until = self.clock.get_time()
        self.shaking = False
        self.shaking_range = 0
        self.shake_speed = 0

    def shake(self, duration: int, range: float, shake_speed: int = 5) -> None:
        """Shakes the camera

        Parameters:
            duration: How long the camera will shake in milliseconds.

        """
        if not self.shaking:
            self.shaking = True
            if self.clock is None:
                current_ticks = pygame.time.get_ticks()
            else:
                current_ticks = self.clock.get_time()

            if duration > 0:
                self.shake_until = current_ticks + duration
            else:
                self.shake_until = None
            self.shaking_range = range
            self.shake_speed = shake_speed

    def update(self, delta_time: float) -> None:
        self.position += self.scroll * delta_time
        self._position += self.scroll * delta_time
        current_ticks = pygame.time.get_ticks()
        if self.shaking:
            shake_vector = pygame.Vector2(
                random.uniform(-self.shaking_range, self.shaking_range),
                random.uniform(-self.shaking_range, self.shaking_range),
            )
            self.move_to_position = self._position + shake_vector

        if self.shake_until is not None and self.shaking and current_ticks >= self.shake_until:
            self.shaking = False
            self.move_to_position = self._position

        self.position = vector2_move_toward(
            self.position, self.move_to_position, self.shake_speed
        )
