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
        return self.sprites[self.current_frame]
    
    def update(self, delta_time):
        if self.time_elapsed >= self.fps:
            self.time_elapsed = 0
            self.current_frame += 1
        
        if self.current_frame == len(self.sprites):
            self.current_frame = 0
        
        self.time_elapsed += delta_time