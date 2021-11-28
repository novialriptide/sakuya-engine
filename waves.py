from random import randrange
from typing import List

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
    def __init__(self, ms_between_waves: int):
        self.waves = [] # List[Wave]
        self.ms_between_waves = ms_between_waves # int
        self.entities = [] # List[Entity]
        self.spawn_points = [] # List[Vector]

    @property
    def rand_entity(self):
        """Returns random entity"""
        return self.entities[randrange(0, len(self.entities))]

    def spawn(self, entity_key: int, spawn_key: int, **kwargs) -> Entity:
        """Handles the entity spawning.
        
        Must be overridden.

        Parameters:

        """

    def load_wave(self, wave: int) -> None:
        pass