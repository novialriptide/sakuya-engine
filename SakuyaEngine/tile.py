"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
import pygame

from typing import List


def crop_tile_image(
    image: pygame.Surface, x: int, y: int, width: int, height: int
) -> pygame.Surface:
    """Crop a tile out.
    Not intended to be used outside of this file.

    Parameters:
        image: A pygame loaded image.
        x: The tile's x position.
        y: The tile's y position.
        width: The tile's width.
        height: The tile's height.

    """
    tile = image.subsurface((x * width, y * height, width, height))

    return tile


def split_image(
    image: pygame.Surface, px_width: int, px_height: int
) -> List[pygame.Surface]:
    """Split an image into a tileset.

    Parameters:
        image: A pygame loaded image.
        px_width: The tile's width in pixels.
        px_height: The tile's height in pixels.
        px_distance: The distance between every tile (WIP).

    """
    rect = image.get_rect()
    columns = int(rect.width / px_width)
    rows = int(rect.height / px_height)
    tiles = []  # List[pygame.Surface]

    for r in range(rows):
        for c in range(columns):
            tile_sprite = crop_tile_image(image, c, r, px_width, px_height)
            tiles.append(tile_sprite)

    return tiles


class TileSet:
    def __init__(self, image: pygame.Surface, px_width: int, px_height: int):
        self.image = image
        self.px_width = px_width
        self.px_height = px_height

        self.tiles = split_image(self.image, self.px_width, self.px_height)


class TileMap:
    def __init__(self, columns: int, rows: int, tile_set: TileSet) -> None:
        self.columns = columns
        self.rows = rows
        self.map_layers = []
        self.tile_set = tile_set
        self._surface = pygame.Surface(  # lgtm [py/call/wrong-arguments]
            columns * tile_set.px_width, rows * tile_set.px_height
        )
        self.add_layer()

    def add_layer(self) -> None:
        layer = []
        for r in range(self.rows):
            layer.append([])
            for c in range(self.columns):
                layer[r][c] = 0
        self.map_layers.append(layer)

    def get_tile(self, layer: int, pos: pygame.Vector2) -> int:
        return self.map_layers[layer][pos.y][pos.x]
