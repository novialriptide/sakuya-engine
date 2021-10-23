import pygame
import typing

class animation:
    def __init__(self, name: str, sprites: typing.List[pygame.sprite.Sprite]):
        self.name = name
        self.sprites = sprites