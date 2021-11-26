import pygame
import typing

class Animation:
    def __init__(
        self,
        name: str,
        sprites: typing.List[pygame.Surface],
        fps: int = 16
    ):
        self.name = name
        self.sprites = sprites
        self.fps = fps
        self.time_elapsed = 0
        self.current_frame = 0
    
    @property
    def sprite(self) -> pygame.Surface:
        return self.sprites[int(self.current_frame)]
    
    def update(self, delta_time):
        self.current_frame += delta_time * self.fps / 60

        if self.current_frame >= len(self.sprites):
            self.current_frame = 0