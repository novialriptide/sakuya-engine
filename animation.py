"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from Helix.SakuyaEngine.tile import split_image

import pygame
import typing
import json

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
        self.is_playing = True
    
    @property
    def sprite(self) -> pygame.Surface:
        return self.sprites[int(self.current_frame)]
    
    def update(self, delta_time):
        if self.is_playing:
            self.current_frame += delta_time * self.fps / 60

            if self.current_frame >= len(self.sprites):
                self.current_frame = 0

def load_anim_dict(data: dict) -> Animation:
    return Animation(
        data["name"],
        sprites = split_image(
            pygame.image.load(data["sprites"]["image"]),
            px_width = data["sprites"]["width"],
            px_height = data["sprites"]["height"]
        ),
        fps = data["fps"]
    )

def load_anim_json(json_path: str) -> Animation:
    data = json.load(open(json_path))

    return load_anim_dict(data)