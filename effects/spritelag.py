"""This effect will leave a trail behind the entity moving around.
"""

import pygame

class _Sprite:
    def __init__(self, sprite: pygame.Sprite, lifetime: int):
        self.lifetime = lifetime
        self.sprite = sprite

class SpriteLag:
    def __init__(self):
        self.sprites = [] # List[pygame.Surface]
        self.temp_sprites = [] # List[_Sprite]