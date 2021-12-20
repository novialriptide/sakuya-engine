"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from random import randrange

from .scene import Scene
from .entity import Entity
from .errors import NotEnoughArgumentsError, NotImplementedError
from .events import EventSystem, WaitEvent

import json

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
        spawn_anim: int,
        lifetime: int,
        events_system: EventSystem
    ) -> Entity:
        """Handles the entity spawning.

        Could be overridden. If not, a premade function
        is already built-in.

        Parameters:
            entity_key: ID of the loaded entity.
            spawn_key: ID of the loaded spawn point.
            spawn_anim: ID of the spawn animation.
            events_system: The scene's event system.

        Returns:
            The spawned entity.

        """
        e = self.entities[entity_key].copy()
        e.position = self.spawn_points[spawn_key] - e.center_position

        return e

    def load_wave(self, wave: int) -> None:
        raise NotImplementedError
    
def _create_spawn_event(
    wave_manager: WaveManager,
    scene: Scene,
    entity_key,
    spawnpoint_key,
    anim_key: int,
    lifetime: int,
    wait_time: int
) -> WaitEvent:
    def spawn_func(_entity_key, _spawnpoint_key, _anim_key, _lifetime, _event_system, _delta_time):
        entity = wave_manager.spawn(_entity_key, _spawnpoint_key, _anim_key, _lifetime, _event_system, _delta_time)
        scene.entities.append(entity)
    spawn_event = WaitEvent("spawn_enemy", wait_time, spawn_func, args=[
        entity_key, spawnpoint_key, anim_key, lifetime,
        scene.event_system, scene.client.get_delta_time
    ])
    return spawn_event
    
def load_wave_file(path: str, wave_manager: WaveManager, scene: Scene) -> None:
    file = open(path, "r")
    wait_time = 0
    for line in file.readlines():
        line = line.replace("\n", "")
        cmd = line.split(" ")
        if cmd[0] == "spawn":
            try:
                spawn_event = _create_spawn_event(wave_manager, scene, int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]), wait_time)
                scene.event_system._methods.append(spawn_event)
            except IndexError:
                raise NotEnoughArgumentsError
        if cmd[0] == "wait":
            wait_time += int(cmd[1])

def load_wave_json(path: str, wave_manager: WaveManager, scene: Scene) -> None:
    file = open(path, "r")
    data = json.load(file)

    raise NotImplementedError