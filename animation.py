import pygame
import typing

class Animation:
    def __init__(
        self,
        name: str,
        sprites: typing.List[pygame.Surface],
        fps: int = 60
    ):
        self.name = name
        self.sprites = sprites
        self.fps = fps