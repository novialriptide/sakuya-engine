from random import randrange
from typing import List

from Helix.Sakuya.scene import Scene

from .entity import Entity
from .errors import NotImplementedError

class Sequence:
    def __init__(self):
        self.in_session = False
        self.entities = [] # List[Entity]

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

    def spawn(
        self,
        entity_key: int,
        spawn_key: int,
    ) -> Entity:
        """Handles the entity spawning.

        Parameters:
            entity_key: ID of the loaded entity.
            spawn_key: ID of the loaded spawn point.

        """
        e = self.entities[entity_key].copy()
        e.position = self.spawn_points[spawn_key] - e.center_position

        return e

    def load_wave(self, wave: int) -> None:
        pass
    
def load_wave_file(path: str, wave_manager: WaveManager, scene: Scene) -> None:
    file = open(path, "r")
    wait_time = 0
    for line in file.readlines():
        line = line.replace("\n", "")
        cmd = line.split(" ")
        if cmd[0] == "spawn":
            e = wave_manager.spawn(int(cmd[1]), int(cmd[2]))
            scene.entities.append(e)