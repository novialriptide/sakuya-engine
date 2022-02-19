"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from SakuyaEngine.__version__ import GAME_VERSION
from pygame import __version__ as pg_ver

__all__ = [
    "ai",
    "animation",
    "bar",
    "bullets",
    "draw",
    "entity",
    "errors",
    "events",
    "lights",
    "math",
    "effect_fire",
    "effect_particles",
    "effect_rain",
    "effects",
    "physics",
    "scene",
    "text",
    "tile",
    "waves",
]

print(
    f"sakuya engine {GAME_VERSION} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya"
)
