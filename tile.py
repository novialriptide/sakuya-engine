import pygame

from typing import List

from .math import Vector
from .errors import NotImplementedError

def crop_tile_image(
    image: pygame.Surface,
    x: int, y: int,
    width: int, height: int
) -> pygame.Surface:
    """
    Crop a tile out.
    Not intended to be used outside of this file.

    Parameters:
        image: A pygame loaded image.
        x: The tile's x position.
        y: The tile's y position.
        width: The tile's width.
        height: The tile's height.

    """
    tile = image.subsurface((x*width, y*height, width, height))

    return tile

def split_image(
    image: pygame.Surface,
    px_width: int,
    px_height: int,
    px_distance: int = 0
) -> List[pygame.Surface]:
    """
    Split an image into a tileset.

    Parameters:
        image: A pygame loaded image.
        px_width: The tile's width in pixels.
        px_height: The tile's height in pixels.
        px_distance: The distance between every tile (WIP).

    """
    rect = image.get_rect()
    columns = int(rect.width / px_width)
    rows = int(rect.height / px_height)
    tiles = [] # List[pygame.Surface]

    for r in range(rows):
        for c in range(columns):
            tiles.append(
                crop_tile_image(
                    image,
                    c, r, 
                    px_width,
                    px_height
                )
            )

    return tiles

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