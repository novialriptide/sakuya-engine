import pygame

from .math import Vector
from .errors import NotImplementedError

def split_image(
    image_path: str,
    px_width: int,
    px_height: int,
    px_distance: int = 0
):
    """
    Split an image into a tileset

    Parameters:
        image_path: The image's path.
        px_width: The tile's width in pixels
        px_height: The tile's height in pixels
        px_distance: The distance between every tile (WIP)
    """

class TileMap:
    def __init__(self):
        self.scale = Vector(1, 1)

class TileSet:
    def __init__(self):
        pass

    @property
    def columns(self):
        raise NotImplementedError

    @property
    def rows(self):
        raise NotImplementedError

class Tile:
    def __init__(self):
        self.sprites = [] # List of pygame.Surfaces
        self.sprite_key = 0 # int