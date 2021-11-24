import pygame

from typing import List

from .math import Vector
from .errors import NotImplementedError

def _get_tile_image(
    image_path: str,
    x: int, y: int,
    width: int, height: int
) -> pygame.Surface:
    """
    Crop a tile out.
    Not intended to be used outside of this file.

    Parameters:
        image_path: The image's path.
        x: The tile's x position.
        y: The tile's y position.
        width: The tile's width.
        height: The tile's height.

    """
    raise NotImplementedError

def split_image(
    image_path: str,
    px_width: int,
    px_height: int,
    px_distance: int = 0
) -> List[pygame.Surface]:
    """
    Split an image into a tileset.

    Parameters:
        image_path: The image's path.
        px_width: The tile's width in pixels.
        px_height: The tile's height in pixels.
        px_distance: The distance between every tile (WIP).

    """
    raise NotImplementedError

class TileMap:
    def __init__(self):
        self.scale = Vector(1, 1)
        raise NotImplementedError

class TileSet:
    def __init__(self):
        raise NotImplementedError

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
        raise NotImplementedError