from typing import List

import random

from .tile import TileMap

class WorldGen:
    def __init__(
        self,
        main_tilemap: TileMap,
        components: List[TileMap],
        seed: int or None = None
    ) -> None:
        self.components = components
        if seed is None:
            self.seed = abs(random.random())
        else:
            self.seed = seed