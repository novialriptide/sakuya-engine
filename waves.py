"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under MIT license (see LICENSE for details)
"""
from random import randrange
from typing import List

from pygame.event import wait

from .scene import Scene

from .entity import Entity
from .errors import NotEnoughArgumentsError, NotImplementedError
from .events import EventSystem, WaitEvent

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
    
def load_wave_file(path: str, wave_manager: WaveManager, scene: Scene) -> None:
    file = open(path, "r")
    wait_time = 0
    for line in file.readlines():
        line = line.replace("\n", "")
        cmd = line.split(" ")
        if cmd[0] == "spawn":
            try:
                def spawn_func(arg0, arg1, arg2, arg3, arg4, arg5):
                    entity = wave_manager.spawn(arg0, arg1, arg2, arg3, arg4, arg5)
                    scene.entities.append(entity)
                    scene.enemies.append(entity)
                spawn_event = WaitEvent("spawn_enemy", wait_time, spawn_func, args=[
                    int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]),
                    scene.event_system, scene.client.get_delta_time
                ])
                scene.event_system._methods.append(spawn_event)
            except IndexError:
                raise NotEnoughArgumentsError
        if cmd[0] == "wait":
            wait_time += int(cmd[1])