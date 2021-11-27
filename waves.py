from random import randrange
from typing import List
from copy import copy

from Helix.Sakuya.entity import Entity
from Helix.Sakuya.math import Vector
from .errors import NotImplementedError

class Wave:
    def __init__(self):
        self.in_session = False

    @property
    def is_all_dead(self):
        return NotImplementedError

class WaveManager:
    def __init__(self, ms_between_waves):
        self.waves = [] # List[Wave]
        self.ms_between_waves = ms_between_waves # int
        self.entities = [] # List[Entity]
        self.spawn_points = [] # List[Vector]

    def spawn(self, entity_key: int) -> Entity:
        raise NotImplementedError

    def generate_random_wave(
        self,
        wave: int,
        entity_scene_list: List[Entity]
    ) -> None:
        raise NotImplementedError
        for sp in self.spawn_points:
            e = self.entities[randrange(0, len(self.entities))]
            e.position = sp - Vector(e.rect.width/2, e.rect.height/2)
            entity_scene_list.append(e.copy())

    def load_wave(self, wave: int) -> None:
        pass