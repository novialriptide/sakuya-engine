import pygame
import typing

class Animation:
    def __init__(
        self,
        sprites: typing.List[pygame.Surface],
        fps: int = 60
    ):
        self.sprites = sprites
        self.fps = fps
    
    @property
    def name() -> str:
        return __name__