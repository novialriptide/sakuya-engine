"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from typing import List

import pygame

__all__ = ["Animation"]


class Animation:
    def __init__(self, name: str, sprites: List[pygame.Surface], fps: int = 16):
        self.name = name
        self.sprites = sprites
        self.fps = fps
        self.time_elapsed = 0
        self.current_frame = 0
        self.is_playing = True

    @property
    def sprite(self) -> pygame.Surface:
        return self.sprites[int(self.current_frame)]

    def update(self, delta_time):
        if self.is_playing:
            self.current_frame += delta_time * self.fps / 60

            if self.current_frame >= len(self.sprites):
                self.current_frame = 0
